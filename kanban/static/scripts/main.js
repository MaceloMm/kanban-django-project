function createInput(name) {
    const newInputEl = document.createElement('input');
    newInputEl.setAttribute('type', 'hidden');
    newInputEl.setAttribute('name', 'task_status');
    newInputEl.setAttribute('value', name);

    return newInputEl;
};

document.getElementById('addNI').addEventListener('click', () => {
    const modalElement = document.getElementById('modalRegister');
    const formElement = document.querySelector('.modalRegister form');
    formElement.appendChild(createInput('NI'));
    modalElement.classList.toggle('hiden');

});

document.getElementById('modalRegister').addEventListener('click', function (e) {
    if (e.target === this) {
        if (this.contains(this.querySelector('[name="tarefa_id"]'))) {
            this.querySelector('form button').removeAttribute('name');
            this.querySelector('form').removeChild(this.querySelector('[name="tarefa_id"]'));
            this.querySelector('[name="title"]').value = "";
            this.querySelector('[name="description"]').innerHTML = "";
        } if (this.contains(this.querySelector('[name="task_status"]'))) {
            this.querySelector('form').removeChild(this.querySelector('[name="task_status"]'));
        };

        this.classList.toggle('hiden');
    };
});

document.querySelectorAll('.editTask').forEach(function (el) {
    el.addEventListener('click', function () {
        const elPai = el.parentElement.parentElement.parentElement.querySelector('main');
        const taskName = elPai.querySelector('div').querySelector('h3').innerText;
        const taskDesc = elPai.querySelector('.desc').innerText;
        const modalEl = document.getElementById('modalRegister');
        const taskId = el.parentElement.querySelector('[name="tarefa_id"]').cloneNode(true);
        modalEl.querySelector('[name="title"]').value = taskName;
        modalEl.querySelector('[name="description"]').innerHTML = taskDesc;
        modalEl.querySelector('form').appendChild(taskId);
        modalEl.querySelector('button').setAttribute('name', 'editTask')

        modalEl.classList.toggle('hiden');
    });
});

document.getElementById('modalDelete').addEventListener('click', function () {
    this.querySelector('form').removeChild(this.querySelector('[name="tarefa_id"]'));
    this.classList.toggle('hiden');
});


document.querySelectorAll('.deleteBtn').forEach(function (el) {
    el.addEventListener('click', function () {
        const inputEl = el.parentElement.querySelector('[name="tarefa_id"]').cloneNode(true);
        const modal = document.getElementById('modalDelete');
        modal.querySelector('form').appendChild(inputEl);
        modal.classList.toggle('hiden')
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const tasks = document.querySelectorAll('.card');
    const containers = document.querySelectorAll('.task_container');
    let draggedItem = null;

    tasks.forEach(task => {
        task.addEventListener('dragstart', dragStart);
        task.addEventListener('dragend', dragEnd);
    });

    containers.forEach(container => {
        container.addEventListener('dragover', dragOver);
        container.addEventListener('dragenter', dragEnter);
        container.addEventListener('dragleave', dragLeave);
        container.addEventListener('drop', drop);
    })

    function dragStart() {
        draggedItem = this;
        setTimeout(() => {
            this.classList.add('dragging');
        }, 0);
    }

    function dragEnd() {
        this.classList.remove('dragging');
    }


    function dragOver(e) {
        e.preventDefault();
    }
    
    function dragEnter(e) {
        e.preventDefault();
        this.classList.add('highlight');
    }
    
    function dragLeave() {
        this.classList.remove('highlight');
    }
    
    function drop() {
        this.classList.remove('highlight');
        
        if (draggedItem.parentElement !== this) {
            this.appendChild(draggedItem);
            
            console.log(draggedItem.getAttribute('name'));
            console.log(`Tarefa foi movida ${this.getAttribute('name')}`);
            
        }
    }

})
