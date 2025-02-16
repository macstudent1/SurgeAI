import '../styles/popup.css';

document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("changeText");
    const text = document.getElementById("displayText");
    document.getElementById("changeColor").addEventListener("click", function () {
        text.textContent = "You clicked the button!";
        text.style.color = "red"; 
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: changePageBackground
            });
        });
    });
});

//function changePageBackground() {
//    document.body.style.backgroundColor = "lightblue";
//}

import '../styles/popup.scss';

document.getElementById('go-to-options').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});