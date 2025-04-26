const csvUrl = 'articles.csv';

function loadArticles() {
  Papa.parse(csvUrl, {
    download: true,
    header: true,
    complete: function(results) {
      const container = document.getElementById('articles');
      results.data.forEach(item => {
        if (!item.title || !item.content) return;
        const card = document.createElement('div');
        card.className = 'article-card';
        card.innerHTML = `
          <h3>${item.title}</h3>
          <p>${item.content}</p>
          ${item.image ? `<img src="${item.image}" alt="${item.title}">` : ''}
        `;
        container.appendChild(card);
      });
    }
  });
}

loadArticles();