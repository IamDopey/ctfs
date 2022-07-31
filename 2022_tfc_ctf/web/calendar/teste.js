
    const text1_options = [
      "Acrylic tubes",
      "Precision made shapes",
      "The best storage solutions",
      "Great insulation"
    ];
    const text2_options = [
      "Amazing colors",
      "Every shape imaginable",
      "That's really satisfying",
      "Warm and cozy"
    ];
    const color_options = ["rgba(82,197,217,0.79)", "#rgba(82,197,217,0.79)", "#rgba(82,197,217,0.79)", "#rgba(82,197,217,0.79)"];
    const image_options = [
      "./static/images/acrylic_tubes.jpeg",
      "./static/images/precision_tubes.jpeg",
      "./static/images/tubes_in_storage.jpeg",
      "./static/images/insulation.jpeg"
    ];
    var i = 0;
    const currentOptionText1 = document.getElementById("current-option-text1");
    const currentOptionText2 = document.getElementById("current-option-text2");
    const currentOptionImage = document.getElementById("image");
    const carousel = document.getElementById("carousel-wrapper");
    const mainMenu = document.getElementById("menu");
    const optionPrevious = document.getElementById("previous-option");
    const optionNext = document.getElementById("next-option");

    currentOptionText1.innerText = text1_options[i];
    currentOptionText2.innerText = text2_options[i];
    currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
    mainMenu.style.background = color_options[i];

    optionNext.onclick = function () {
      i = i + 1;
      i = i % text1_options.length;
      currentOptionText1.dataset.nextText = text1_options[i];

      currentOptionText2.dataset.nextText = text2_options[i];

      mainMenu.style.background = color_options[i];
      carousel.classList.add("anim-next");

      setTimeout(() => {
        currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
      }, 455);

      setTimeout(() => {
        currentOptionText1.innerText = text1_options[i];
        currentOptionText2.innerText = text2_options[i];
        carousel.classList.remove("anim-next");
      }, 650);
    };

    optionPrevious.onclick = function () {
      if (i === 0) {
        i = text1_options.length;
      }
      i = i - 1;
      currentOptionText1.dataset.previousText = text1_options[i];

      currentOptionText2.dataset.previousText = text2_options[i];

      mainMenu.style.background = color_options[i];
      carousel.classList.add("anim-previous");

      setTimeout(() => {
        currentOptionImage.style.backgroundImage = "url(" + image_options[i] + ")";
      }, 455);

      setTimeout(() => {
        currentOptionText1.innerText = text1_options[i];
        currentOptionText2.innerText = text2_options[i];
        carousel.classList.remove("anim-previous");
      }, 650);
    };
  