document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("myForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the form from submitting by default

        // Get the values from the input fields
        const weight1 = parseFloat(document.getElementById("weight_1").value);
        const weight2 = parseFloat(document.getElementById("weight_2").value);


        // Check if the sum is approximately equal to 1 (considering floating-point precision)
        const sum = weight1  + weight2;
        if (Math.abs(sum - 1) < 0.0001) {
            // The sum is close enough to 1, so allow the form to submit
            form.submit();
        } else {
            // The sum is not equal to 1, so display an error message
            alert("The values must add up to 1.");
        }
    });
});
