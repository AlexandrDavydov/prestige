function capitalizeFirst(input) {
    if (input.value.length > 0) {
        input.value =
            input.value.charAt(0).toUpperCase() +
            input.value.slice(1);
    }
}