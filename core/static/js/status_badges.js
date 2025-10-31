document.addEventListener('DOMContentLoaded', function () {
  const map = {
    'SOLICITADO': 'status-solicitado',
    'CONFIRMADO': 'status-confirmado',
    'REALIZADO': 'status-realizado',
    'CANCELADO': 'status-cancelado'
  };

  function updateSelectBadge(select) {
    // apply classes directly on the select so the colored background sits only on the rounded badge
    if (!select) return;
    // remove existing status- classes from select
    select.classList.remove('status-solicitado','status-confirmado','status-realizado','status-cancelado');
    const cls = map[select.value];
    if (cls) select.classList.add(cls);
  }

  // initialize all selects on the page
  document.querySelectorAll('td.status-cell select[name="status"]').forEach(function (sel) {
    updateSelectBadge(sel);
    sel.addEventListener('change', function () {
      updateSelectBadge(sel);
      // After selection, force blur so the :focus styles (white background) are removed
      // Delay a bit to allow native selection UI to complete on some browsers
      setTimeout(function () {
        try {
          sel.blur();
        } catch (e) {
          // ignore
        }
        updateSelectBadge(sel);
      }, 60);
    });
  });
});
