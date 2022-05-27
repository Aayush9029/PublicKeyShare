const getURLKey = () => {
  const url = window.location.href;
  const urlKey = url.split('?')[1];
  return urlKey;
};

const fetchData = async () => {
  let apiURL = "http://127.0.0.1:80/" + getURLKey() + "/";
  console.log(apiURL);
  const response = await fetch(apiURL);
  const data = await response.json();
  return data;
};

const getSelector = (selectorName) => {
  return document.querySelector(selectorName);
};

const copyToClipboard = (selector) => {
  let text = selector.innerText;
  if (text === "" || text === null) {
    text = selector.value;
  }
  navigator.clipboard.writeText(text);
  console.log('Copied to clipboard: ' + text);
}

const addCopyEvent = (selector) => {
  selector.addEventListener("click", (e) => {
    copyToClipboard(selector);
  });
};

const populateViews = (data) => {
  let title = getSelector('#data-title');
  let publickey = getSelector('#data-pubkey');
  let sha512 = getSelector('#data-sha512');
  let key = getSelector('#data-key');

  title.innerHTML = data.title;
  publickey.innerHTML = data.publickey;
  sha512.innerHTML = data.hash;
  key.value = data.key;

  addCopyEvent(publickey);
  addCopyEvent(sha512);
}


// for cool animation
const showHiddenInput = (inputOverlay, inputPass, inputIcon) => {
  const overlay = document.getElementById(inputOverlay),
    input = document.getElementById(inputPass),
    iconEye = document.getElementById(inputIcon);

  iconEye.addEventListener("click", () => {
    if (input.type === "password") {
      input.type = "text";
      iconEye.classList.add("bx-show");
    } else {
      input.type = "password";
      iconEye.classList.remove("bx-show");
    }
    overlay.classList.toggle("overlay-content");
  });
};


// main
window.onload = function () {
  console.log('view.js loaded');
  showHiddenInput("input-overlay", "data-key", "input-icon");

  let fetchedData = fetchData('SgzFZB8Rqj');
  fetchedData.then(data => {
    console.log(data);
    populateViews(data);
  });
};
