chrome.runtime.onInstalled.addListener(() => {
    // disable the action by default
    chrome.action.disable();
    chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
        chrome.declarativeContent.onPageChanged.addRules([
            {
                // define the rule's conditions
                conditions: [
                    new chrome.declarativeContent.PageStateMatcher({
                        pageUrl: { urlMatches: "twitter.com/[^/]+/[^/]+/" },
                    }),
                    new chrome.declarativeContent.PageStateMatcher({
                        pageUrl: { hostSuffix: "http://127.0.0.1:8080/inference" }
                    })
                ],
                // show the action when conditions are met
                actions: [new chrome.declarativeContent.ShowPageAction()],
            },
        ]);
    });
});