document.addEventListener('DOMContentLoaded', function() {
  const sortSelect = document.getElementById('sort-select');
  const categorySelect = document.getElementById('category-select');
  const loadMoreBtn = document.getElementById('load-more');

  if (sortSelect) {
    sortSelect.addEventListener('change', updateUrl);
  }
  if (categorySelect) {
    categorySelect.addEventListener('change', updateUrl);
  }

  function updateUrl() {
    let baseUrl = '/';
    const category = categorySelect ? categorySelect.value : '';
    if (category) {
      baseUrl = `/category/${category}/`;
    }
    let params = new URLSearchParams();
    const sort = sortSelect ? sortSelect.value : '';
    if (sort) params.append('sort', sort);
    const q = new URLSearchParams(window.location.search).get('q');
    if (q) params.append('q', q);
    const queryString = params.toString();
    window.location.href = baseUrl + (queryString ? '?' + queryString : '');
  }

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function() {
      const nextPage = this.dataset.page;
      const currentUrl = new URL(window.location.href);
      currentUrl.searchParams.set('page', nextPage);
      currentUrl.searchParams.set('ajax', '1');
      fetch(currentUrl)
        .then(response => response.text())
        .then(html => {
          document.querySelector('.products-grid').insertAdjacentHTML('beforeend', html);
          this.dataset.page = parseInt(nextPage) + 1;
          if (html.trim() === '') {
            this.style.display = 'none';
          }
        });
    });
  }
});