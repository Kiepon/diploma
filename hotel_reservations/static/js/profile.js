// document.getElementById('UpdateForm').addEventListener('submit', (event) => {
//     event.preventDefault(); // Предотвращаем стандартную отправку формы

//     // Получаем данные формы
//     const form = event.target;
//     const formData = new FormData(form);

//     // Отправляем данные на сервер через fetch
//     fetch(form.action, {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => {
//         if (response.ok) {
//             document.getElementById('successMessage').style.display = 'block';
//             setTimeout(() => {
//                 document.getElementById('successMessage').style.display = 'none';
//             }, 3000);
//         } else {
//             throw new Error('Ошибка при обновлении данных');
//         }
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         alert('Произошла ошибка при обновлении данных');
//     });
// });