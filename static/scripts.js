let input = document.querySelector('input')
let button = document.getElementById('submit')

input.addEventListener('change', updateValue)

function updateValue(e) {
  button.disabled = (e.target.value === '')
}

button.addEventListener("click", onButtonTap)

function onButtonTap(e) {
  changeState(true)
}

function changeState(isLoading) {
  input.disabled = isLoading
  button.disabled = !isLoading
}

