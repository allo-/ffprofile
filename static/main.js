// Javascript to enable link to tab
const links = document.querySelectorAll(".nav a");
const active = { link: links[0].parentElement, form: document.getElementById("start") }
let old_hash = "";

function setActive(link, form) {
    active.link.classList.remove("active");
    active.form.classList.remove("active");

    link.classList.add("active");
    form.classList.add("active");
    
    active.link = link;
    active.form = form;
}

function showCurrentForm() {
    const id = location.hash || "#start";
    const form = document.getElementById(id.substr(1));

    for (const link of links) {
        if (link.href.endsWith(id)) {
            setActive(link.parentElement, form);
            break;
        }
    }
}

// Focus form after POST/hash change/nav link click. 
// Feels a little hacky, but I have no idea how to do it any other way
window.addEventListener("load", showCurrentForm);
window.addEventListener("hashchange", showCurrentForm);
links.forEach(l => l.addEventListener("click", showCurrentForm));

const modeTransitions = [
    "background-color .5s ease-in",
    "color .5s ease-in",
    "border-color .5s ease-in",
    "fill .5s ease-in",
    "stroke .5s ease-in",
];

let darkMode = document.body.classList.contains("dark-colors");

function setDarkMode(on, transition=true) {
    document.cookie = "theme=" + (on ? "dark" : "light");

    if (transition) {
        // Enable global transitions for the duration of the change
        const oldTransition = document.body.style.transition;
        document.body.style.transition = modeTransitions.join(",");
        setTimeout(() => document.body.style.transition = oldTransition, 510);
    }

    let classes = ["light-colors", "dark-colors"];
    if (on) classes = classes.reverse()

    document.body.classList.add(classes[0]);
    document.body.classList.remove(classes[1]);
}

document
.getElementById("darkmode-toggle")
.addEventListener("click", () => {
    darkMode = !darkMode;
    setDarkMode(darkMode);
});