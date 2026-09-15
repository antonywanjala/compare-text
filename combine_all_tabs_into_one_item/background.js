chrome.action.onClicked.addListener(async (currentTab) => {
  // Identify the window where you clicked the extension
  const targetWindowId = currentTab.windowId;

  // Grab every open tab across all of Chrome
  const allTabs = await chrome.tabs.query({});

  // Filter for tabs that are NOT in your current window
  const tabsToMove = allTabs.filter(tab => tab.windowId !== targetWindowId);
  const tabIds = tabsToMove.map(tab => tab.id);

  if (tabIds.length > 0) {
    // Move all those tabs to the end of your current window
    await chrome.tabs.move(tabIds, { 
      windowId: targetWindowId, 
      index: -1 
    });
  }
});