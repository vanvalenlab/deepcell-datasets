import passwordValidator from 'password-validator';

const PasswordSchema = new passwordValidator();

// Add properties to it
PasswordSchema.is()
  .min(8) // Minimum length 8
  .is()
  .max(128) // Maximum length 128
  .has()
  .uppercase() // Must have uppercase letters
  .has()
  .lowercase() // Must have lowercase letters
  .has()
  .digits() // Must have at least 1 digit
  .has()
  .symbols(); // Must have at least 1 symbol

export default PasswordSchema;
