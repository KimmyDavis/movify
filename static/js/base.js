const containers = [...document.querySelectorAll(".scroll-horizontal")];
for (let container of containers) {
  container.addEventListener("wheel", function (e) {
    container.scrollLeft += e.deltaY / 10;
  });
  const moveEvent = (e) => {
    e.preventDefault();
    container.scrollLeft += 1.5 * (initPos - e.pageX);
    initPos = e.pageX;
  };

  container.addEventListener("mousedown", (e) => {
    e.preventDefault();
    initPos = e.pageX;
    container.addEventListener("mousemove", moveEvent);
  });

  container.addEventListener("mouseup", (e) => {
    container.removeEventListener("mousemove", moveEvent);
  });
  container.addEventListener("mouseleave", () => {
    container.removeEventListener("mousemove", moveEvent);
  });
}

const menuToggle = document.querySelector(".toggle");
const footer = document.querySelector(".footer");
menuToggle.addEventListener("click", () => {
  let faChild = menuToggle.querySelector(".fa");
  if (menuToggle.classList.contains("active")) {
    menuToggle.classList.remove("active");
    faChild.classList.remove("fa-times");
    faChild.classList.add("fa-bars");
    footer.classList.remove("hide");
  } else {
    menuToggle.classList.add("active");
    faChild.classList.remove("fa-bars");
    faChild.classList.add("fa-times");
    footer.classList.add("hide");
  }
});
