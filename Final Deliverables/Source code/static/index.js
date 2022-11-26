let menu = document.getElementById("menu");
let links = document.getElementById("nav_links");
let body = document.getElementById("body");

menu.addEventListener("click", ()=>{
    links.classList.toggle("nav_responsive");
    links.classList.toggle("navbac");
    body.classList.toggle("bacdrop");
});