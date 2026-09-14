(function () {
    'use strict';

    function goBack(fallback) {
        if (window.history.length > 1 && document.referrer && document.referrer !== window.location.href) {
            window.history.back();
        } else {
            window.location.href = fallback || 'index.html';
        }
    }

    function bindBackButtons() {
        const buttons = document.querySelectorAll('[data-action="back"]');
        buttons.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const fallback = btn.getAttribute('data-fallback') || 'overview.html';
                goBack(fallback);
            });
        });
    }

    function bindClickableCards() {
        const cards = document.querySelectorAll('.card[data-href]');
        cards.forEach(function (card) {
            card.classList.add('is-clickable');
            card.setAttribute('role', 'link');
            card.setAttribute('tabindex', '0');
            const href = card.getAttribute('data-href');

            card.addEventListener('click', function () {
                window.location.href = href;
            });
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    window.location.href = href;
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        bindBackButtons();
        bindClickableCards();
    });
})();
