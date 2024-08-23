const openModalBtn = document.getElementById('openModal');
const closeModalBtns = document.querySelectorAll('#myModal .btn-close');

const modal = document.getElementById('myModal');

openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
});

function openModal(id){
    const modal = document.getElementById(id);
    modal.style.display = 'block';
}

function closeModal(id){
    const modal = document.getElementById(id);
    modal.style.display = 'none';
}