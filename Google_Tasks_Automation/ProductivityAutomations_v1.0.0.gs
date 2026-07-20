/**
 * Productivity Automations (V2)
 * Features: Circuit Breakers, Specific Day Scheduling, Weekly Metrics, Respawn Suppression
 */

const CONFIG = {
  SPREADSHEET_URL: SpreadsheetApp.getActiveSpreadsheet() ? SpreadsheetApp.getActiveSpreadsheet().getUrl() : "", 
  CALENDAR_EVENT_TITLE: "Daily Briefing",
  DAILY_EXECUTION_HOUR: 4, 
  SUNDAY_REVIEW_HOUR: 6,
  MAX_OPEN_TASKS_PER_LIST: 3
};

/**
 * Run this function ONCE to set up the automated triggers.
 */
function setupTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (let i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  ScriptApp.newTrigger('generateDailyTasks').timeBased().everyDays(1).atHour(CONFIG.DAILY_EXECUTION_HOUR).create();
  ScriptApp.newTrigger('generateSundayReview').timeBased().onWeekDay(ScriptApp.WeekDay.SUNDAY).atHour(CONFIG.SUNDAY_REVIEW_HOUR).create();
  Logger.log("Triggers configured successfully!");
}

function getTaskListId(listName) {
  if (listName === "@default") return "@default";
  const cache = PropertiesService.getUserProperties();
  const cachedId = cache.getProperty("TASK_LIST_" + listName);
  if (cachedId) {
    try { Tasks.Tasklists.get(cachedId); return cachedId; } 
    catch(e) { cache.deleteProperty("TASK_LIST_" + listName); }
  }
  let pageToken;
  do {
    const response = Tasks.Tasklists.list({maxResults: 100, pageToken: pageToken});
    if (response.items) {
      for (let i = 0; i < response.items.length; i++) {
        if (response.items[i].title === listName) {
          cache.setProperty("TASK_LIST_" + listName, response.items[i].id);
          return response.items[i].id;
        }
      }
    }
    pageToken = response.nextPageToken;
  } while (pageToken);
  const newList = Tasks.Tasklists.insert({title: listName});
  cache.setProperty("TASK_LIST_" + listName, newList.id);
  return newList.id;
}

// Global caches for the daily run
let listTaskCounts = {};
let completedTaskCache = {};

function countActiveTasks(listId) {
  if (listTaskCounts[listId] !== undefined) return listTaskCounts[listId];
  let count = 0;
  let pageToken;
  do {
    const response = Tasks.Tasks.list(listId, {showCompleted: false, maxResults: 100, pageToken: pageToken});
    if (response.items) count += response.items.length;
    pageToken = response.nextPageToken;
  } while (pageToken);
  listTaskCounts[listId] = count;
  return count;
}

function wasCompletedRecently(taskTitle, listId) {
  if (!completedTaskCache[listId]) {
    completedTaskCache[listId] = [];
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    let pageToken;
    do {
      const response = Tasks.Tasks.list(listId, {showCompleted: true, showHidden: true, updatedMin: sevenDaysAgo.toISOString(), maxResults: 100, pageToken: pageToken});
      if (response.items) {
        response.items.forEach(t => {
          if (t.status === 'completed') completedTaskCache[listId].push(t.title);
        });
      }
      pageToken = response.nextPageToken;
    } while (pageToken);
  }
  return completedTaskCache[listId].indexOf(taskTitle) !== -1;
}

function ensureTaskExistsAndAllowed(taskTitle, taskNotes, listId, isOneOff) {
  // 1. Circuit Breaker Check
  let activeCount = countActiveTasks(listId);
  if (activeCount >= CONFIG.MAX_OPEN_TASKS_PER_LIST) {
    return { success: false, reason: "CIRCUIT_BREAKER" };
  }

  // 2. Active Duplicate Check
  let pageToken;
  do {
    const response = Tasks.Tasks.list(listId, {showCompleted: false, maxResults: 100, pageToken: pageToken});
    if (response.items) {
      for (let i = 0; i < response.items.length; i++) {
        if (response.items[i].title === taskTitle) return { success: false, reason: "ALREADY_ACTIVE" };
      }
    }
    pageToken = response.nextPageToken;
  } while (pageToken);
  
  // 3. Respawn Suppression (Only for one-off Project Tasks)
  if (isOneOff && wasCompletedRecently(taskTitle, listId)) {
    return { success: false, reason: "RECENTLY_COMPLETED" };
  }
  
  // Passed all checks, insert it
  if (taskNotes) Tasks.Tasks.insert({title: taskTitle, notes: taskNotes}, listId);
  else Tasks.Tasks.insert({title: taskTitle}, listId);
  
  listTaskCounts[listId]++; // increment active count cache
  return { success: true };
}

function generateDailyTasks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error("Could not access spreadsheet.");
  
  let briefText = "Good morning! Here is your daily productivity brief:\n\n";
  let totalTasksAdded = 0;
  
  const today = new Date();
  const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const currentDayName = dayNames[today.getDay()];

  // 1. Recurring Habits
  const habitsSheet = ss.getSheetByName("Recurring Habits");
  const habitsData = habitsSheet.getDataRange().getValues();
  for (let i = 1; i < habitsData.length; i++) {
    let [category, goalName, freq, target, type, isActive] = habitsData[i];
    if (isActive === true && (freq === "Daily" || freq === currentDayName)) {
      let taskTitle = `[Habit] ${goalName} (Target: ${target} ${type})`;
      let res = ensureTaskExistsAndAllowed(taskTitle, null, getTaskListId(category), false);
      if (res.reason !== "CIRCUIT_BREAKER") briefText += `- ${taskTitle}\n`;
      totalTasksAdded++;
    }
  }

  // 2. Project Backlog (Next Actions)
  const backlogSheet = ss.getSheetByName("Project Backlog");
  const backlogData = backlogSheet.getDataRange().getValues();
  for (let i = 1; i < backlogData.length; i++) {
    let [category, project, taskName, status, priority, notes] = backlogData[i];
    if (status === "Next Action") {
      let taskTitle = `[Project: ${project}] ${taskName}`;
      let res = ensureTaskExistsAndAllowed(taskTitle, notes, getTaskListId(category), true);
      if (res.reason !== "CIRCUIT_BREAKER" && res.reason !== "RECENTLY_COMPLETED") {
        briefText += `- ${taskTitle}\n`;
        totalTasksAdded++;
      }
    }
  }

  // 3. Household Cleaning (Pop Top Priority)
  const cleanSheet = ss.getSheetByName("Household Cleaning Queue");
  const cleanData = cleanSheet.getDataRange().getValues();
  let cleanItems = [];
  for (let i = 1; i < cleanData.length; i++) {
    cleanItems.push({row: i+1, area: cleanData[i][0], priority: cleanData[i][1], urgent: cleanData[i][2]});
  }
  cleanItems.sort((a, b) => a.priority - b.priority);
  
  if (cleanItems.length > 0) {
    let topItem = cleanItems[0];
    let taskTitle = `[Household] Deep Clean: ${topItem.area}`;
    let res = ensureTaskExistsAndAllowed(taskTitle, null, getTaskListId("Household"), false);
    
    if (res.reason !== "CIRCUIT_BREAKER") {
      briefText += `- ${taskTitle}\n`;
      cleanSheet.getRange(topItem.row, 2).setValue(999);
      cleanSheet.getRange(topItem.row, 4).setValue(new Date());
      totalTasksAdded++;
    }
  }

  if (totalTasksAdded > 0) {
    CalendarApp.getDefaultCalendar().createAllDayEvent(CONFIG.CALENDAR_EVENT_TITLE, today, {description: briefText});
  }
}

/**
 * CORE LOGIC: Sunday Review (V2 Weekly Metrics)
 */
function generateSundayReview() {
  let reviewText = "WEEKLY REVIEW DATA\n\n";
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
  
  // 1. Weekly Progress Metrics
  reviewText += "--- HABIT ADHERENCE (LAST 7 DAYS) ---\n";
  let completedCounts = {};
  
  let listToken;
  do {
    const listResp = Tasks.Tasklists.list({maxResults: 100, pageToken: listToken});
    if (listResp.items) {
      listResp.items.forEach(list => {
        let pageToken;
        do {
          const tasksResp = Tasks.Tasks.list(list.id, {showCompleted: true, showHidden: true, updatedMin: sevenDaysAgo.toISOString(), maxResults: 100, pageToken: pageToken});
          if (tasksResp.items) {
            tasksResp.items.forEach(t => {
              if (t.status === 'completed' && t.title.startsWith("[Habit]")) {
                completedCounts[t.title] = (completedCounts[t.title] || 0) + 1;
              }
            });
          }
          pageToken = tasksResp.nextPageToken;
        } while (pageToken);
      });
    }
    listToken = listResp.nextPageToken;
  } while (listToken);

  const keys = Object.keys(completedCounts);
  if (keys.length === 0) reviewText += "No habits completed this week.\n";
  keys.forEach(k => reviewText += `${k}: ${completedCounts[k]} completions\n`);
  
  // 2. Scrape @default Inbox
  reviewText += "\n--- INBOX (VOICE CAPTURES) ---\n";
  let inboxItems = [];
  let pageToken;
  do {
    const response = Tasks.Tasks.list('@default', {showCompleted: false, maxResults: 100, pageToken: pageToken});
    if (response.items) response.items.forEach(task => inboxItems.push(task.title));
    pageToken = response.nextPageToken;
  } while (pageToken);

  if (inboxItems.length === 0) reviewText += "No new items captured this week.\n";
  inboxItems.forEach(i => reviewText += "- " + i + "\n");
  
  reviewText += "\n--- INSTRUCTIONS ---\n";
  reviewText += "Paste this entire block into Gemini and say: 'Help me review this data and tell me what metrics to update in my Google Sheet.'";
  
  const today = new Date();
  CalendarApp.getDefaultCalendar().createEvent("SUNDAY REVIEW PREP", 
    new Date(today.getFullYear(), today.getMonth(), today.getDate(), 7, 0),
    new Date(today.getFullYear(), today.getMonth(), today.getDate(), 8, 0),
    {description: reviewText}
  );
}
