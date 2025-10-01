/**
 * Sistema de Notificações Toast
 * Inspirado no sistema de flash messages do projeto CaseBem
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Criar container se não existir
        if (!document.getElementById('toast-container')) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container position-fixed top-0 end-0 p-3';
            this.container.style.zIndex = '9999';
            document.body.appendChild(this.container);
        } else {
            this.container = document.getElementById('toast-container');
        }
    }

    /**
     * Mostra um toast
     * @param {string} message - Mensagem a ser exibida
     * @param {string} type - Tipo do toast (success, error, warning, info)
     * @param {string} title - Título do toast
     * @param {number} duration - Duração em milissegundos
     */
    show(message, type = 'info', title = 'Notificação', duration = 5000) {
        // Criar elemento do toast
        const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast align-items-center border-0 toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        // Ícones para cada tipo
        const icons = {
            success: '<i class="bi bi-check-circle-fill me-2"></i>',
            error: '<i class="bi bi-x-circle-fill me-2"></i>',
            warning: '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
            info: '<i class="bi bi-info-circle-fill me-2"></i>'
        };

        const icon = icons[type] || icons.info;

        toast.innerHTML = `
            <div class="toast-header">
                ${icon}
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        // Adicionar ao container
        this.container.appendChild(toast);

        // Inicializar e mostrar o toast do Bootstrap
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: duration
        });
        bsToast.show();

        // Remover do DOM após fechar
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    /**
     * Mostra um toast de sucesso
     */
    success(message, title = 'Sucesso', duration = 5000) {
        this.show(message, 'success', title, duration);
    }

    /**
     * Mostra um toast de erro
     */
    error(message, title = 'Erro', duration = 5000) {
        this.show(message, 'error', title, duration);
    }

    /**
     * Mostra um toast de aviso
     */
    warning(message, title = 'Atenção', duration = 5000) {
        this.show(message, 'warning', title, duration);
    }

    /**
     * Mostra um toast de informação
     */
    info(message, title = 'Informação', duration = 5000) {
        this.show(message, 'info', title, duration);
    }
}

// Instância global do gerenciador de toasts
const toastManager = new ToastManager();

/**
 * Processa toasts injetados pelo backend
 */
function processServerToasts() {
    // Buscar toasts injetados pelo servidor
    const toastsData = document.getElementById('server-toasts-data');

    if (toastsData) {
        try {
            const toasts = JSON.parse(toastsData.textContent);

            // Mostrar cada toast
            toasts.forEach(toast => {
                toastManager.show(
                    toast.message,
                    toast.type,
                    toast.title,
                    toast.duration
                );
            });
        } catch (e) {
            console.error('Erro ao processar toasts do servidor:', e);
        }
    }
}

// Processar toasts quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processServerToasts);
} else {
    processServerToasts();
}

// Exportar para uso global
window.toast = toastManager;
