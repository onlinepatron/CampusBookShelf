function validatePassword(password) {
    let minLength = 8;
    let hasUpperCase = /[A-Z]/.test(password);
    let hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    let hasNumber = /[0-9]/.test(password);

    if (password.length < minLength || !hasUpperCase || !hasSpecialChar || !hasNumber) {
        return false;
    }
    return true;
}
