
function bracketButton() {
    const bracketInput = $('#bracket-input');
    const inputValue = bracketInput.val();
    const reg = /^[\{\}\[\]\(\)]+$/
    if (!reg.test(inputValue)) {
        alert('Please enter a string that only contains the follow characters: "{", "}", "(", ")", "[", "]".');
        bracketInput.val('');
    } else {
        $.post('/brackets', {"data": inputValue}, (returnData) => {
            $('#bracket-label').text(returnData);
        })
    }
}
