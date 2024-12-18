// Definindo o conjunto globalmente para armazenar os IDs das notificações já exibidas
const displayedNotifications = new Set();

// Função para fazer a requisição e adicionar novas notificações no início da lista
function checkNotifications() {
    fetch('/notificacoes/check/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta da requisição');
            }
            return response.json();
        })
        .then(data => {
            if (data.status) {
                const notificationCount = document.querySelector('.icon-badge');
                const notificationsContent = document.getElementById('notifications-content');
                
                // Atualizando o contador de notificações
                const newNotificationsCount = displayedNotifications.size + data.notificacoes.length;
                notificationCount.innerText = newNotificationsCount;

                // Adicionando a animação ao ícone de notificação
                if (newNotificationsCount > 0) {
                    notificationCount.classList.add('new-notification');
                } else {
                    notificationCount.classList.remove('new-notification');
                }

                // Adicionando apenas novas notificações no início da lista
                data.notificacoes.forEach(notification => {
                    if (!displayedNotifications.has(notification.id)) {
                        displayedNotifications.add(notification.id);

                        const notificationHtml = `
                            <div class="item p-3 new" data-id="${notification.id}">
                                <div class="row gx-2 justify-content-between align-items-center">
                                    <div class="col-auto">
                                        <div class="app-icon-holder icon-holder-mono">
                                            ${notification.icone.includes('fa-') ? 
                                                `<i class="${notification.icone}"></i>` : 
                                                `<img class="profile-image" src="${notification.icone}" alt="">`}
                                        </div>
                                    </div>
                                    <div class="col">
                                        <div class="info">
                                            <div class="desc">${notification.msg}</div>
                                            <div class="meta">Agora mesmo</div>
                                        </div>
                                    </div>
                                </div>
                                <a class="link-mask" href="${notification.link}"></a>
                            </div>
                        `;
                        notificationsContent.insertAdjacentHTML('afterbegin', notificationHtml);
                    }
                });
            } else {
                console.log('Sem novas notificações');
            }
        })
        .catch(error => console.error('Erro ao verificar notificações:', error));
}

function markAllAsRead() {
    // Pega todos os elementos com a classe 'new'
    const newNotifications = document.querySelectorAll('.item.new');
    const notificationIds = Array.from(newNotifications).map(notification => notification.getAttribute('data-id'));

    // Envia a lista de IDs para o Django via POST
    fetch('/notificacoes/marcar_como_lida/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Certifique-se de que o CSRF Token está configurado
        },
        body: JSON.stringify({ ids: notificationIds })
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro ao marcar notificações como lidas');
        
        // Remover a classe 'new' dos elementos e adicionar a classe 'lida'
        newNotifications.forEach(notification => {
            notification.classList.remove('new');
            notification.classList.add('lida'); // Opcional: classe para indicar visualmente que está lida
        });

        // Zerar o contador de notificações
        const notificationCount = document.querySelector('.icon-badge');
        notificationCount.innerText = 0;
        notificationCount.classList.remove('new-notification'); // Remove animação do ícone
    })
    .catch(error => console.error('Erro ao marcar notificações como lidas:', error));
}

// Configura o intervalo de 10 segundos (10000 ms) para verificar novas notificações
setInterval(checkNotifications, 10000);
