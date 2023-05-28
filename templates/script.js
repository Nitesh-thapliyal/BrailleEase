document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.getElementById("text-input");
    const brailleOutput = document.getElementById("braille-output");
  
    const clearText = () => {
      textInput.value = "";
      brailleOutput.value = "";
    };
  
    const copyToClipboard = () => {
      navigator.clipboard.writeText(brailleOutput.value);
    };
  
    const handleOnChange = () => {
      const text = textInput.value;
      const brailleText = convertToBraille(text);
      brailleOutput.value = brailleText;
    };
  
    textInput.addEventListener("input", handleOnChange);
  });
  