function createInput(name){
    const newInputEl = document.createElement('input');
    newInputEl.setAttribute('type', 'hidden');
    newInputEl.setAttribute('name', 'task_status');
    newInputEl.setAttribute('value', name);

    return newInputEl;
}

document.getElementById('addNI').addEventListener('click', () => {
    const modalElement = document.getElementById('modalRegister');
    const formElement = document.querySelector('.modalRegister form');
    formElement.appendChild(createInput('NI'));
    modalElement.classList.toggle('hiden');

})

document.getElementById('modalRegister').addEventListener('click', function(e) {
    if (e.target === this){this.classList.toggle('hiden');};
})

document.querySelectorAll('.editTask').forEach(function (el){
    el.addEventListener('click', function(){
        const elPai = el.parentElement.parentElement.parentElement.querySelector('main');
        const taskName = elPai.querySelector('div').querySelector('h3').innerText;
        const taskDesc = elPai.querySelector('.desc').innerText;
        const modalEl = document.getElementById('modalRegister');
        const taskId = el.parentElement.querySelector('[name="tarefa_id"]')
        modalEl.querySelector('[name="title"]').value = taskName;
        modalEl.querySelector('[name="description"]').innerHTML = taskDesc;
        modalEl.querySelector('form').appendChild(taskId);
        modalEl.querySelector('button').setAttribute('name', 'editTask')

        modalEl.classList.toggle('hiden');
    })
})