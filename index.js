let sp = document.querySelector(".signup");
let login = document.querySelector(".login");
let sl = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");

sp.addEventListener("click", () => {
	sl.classList.add("moveslider");
	formSection.classList.add("form-section-move");
});

login.addEventListener("click", () => {
	sl.classList.remove("moveslider");
	formSection.classList.remove("form-section-move");
});
