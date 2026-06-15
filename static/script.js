document.addEventListener("DOMContentLoaded", () => {

    const inputs =
    document.querySelectorAll(".bit-input");

    inputs.forEach(input => {

        input.addEventListener("input", () => {

            input.value =
            input.value.replace(/[^01]/g,'');

        });

    });

});