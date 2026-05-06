import * as params from '@params';

let fuse;
let first;
let last;
let currentElem = null;
let resultsAvailable = false;

const resList = document.getElementById('searchResults');
const sInput = document.getElementById('searchInput');
const statusNode = document.getElementById('searchStatus');
const fuseOpts = params.fuseOpts || {};
const resultLimit = fuseOpts.limit || 12;

const defaultKeys = [
    { name: 'title', weight: 0.42 },
    { name: 'summary', weight: 0.24 },
    { name: 'content', weight: 0.32 },
    { name: 'permalink', weight: 0.02 }
];

const options = {
    isCaseSensitive: fuseOpts.iscasesensitive ?? false,
    includeScore: fuseOpts.includescore ?? false,
    includeMatches: true,
    minMatchCharLength: fuseOpts.minmatchcharlength ?? 1,
    shouldSort: fuseOpts.shouldsort ?? true,
    findAllMatches: fuseOpts.findallmatches ?? true,
    keys: fuseOpts.keys ?? defaultKeys,
    location: fuseOpts.location ?? 0,
    threshold: fuseOpts.threshold ?? 0.35,
    distance: fuseOpts.distance ?? 120,
    ignoreLocation: fuseOpts.ignorelocation ?? true
};

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, function (char) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[char];
    });
}

function escapeRegex(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function textOnly(value) {
    const div = document.createElement('div');
    div.innerHTML = String(value ?? '');
    return (div.textContent || div.innerText || '').replace(/\s+/g, ' ').trim();
}

function getTerms(query) {
    return query.trim().split(/\s+/).filter(Boolean).slice(0, 6);
}

function findTermIndex(text, terms) {
    const lowerText = text.toLocaleLowerCase();
    for (const term of terms) {
        const index = lowerText.indexOf(term.toLocaleLowerCase());
        if (index >= 0) return { index, term };
    }
    return { index: 0, term: '' };
}

function highlightText(text, query) {
    const terms = getTerms(query).sort((a, b) => b.length - a.length);
    const escaped = escapeHtml(text);
    if (!terms.length) return escaped;

    const pattern = new RegExp('(' + terms.map(escapeRegex).join('|') + ')', 'gi');
    return escaped.replace(pattern, '<mark class="search-highlight">$1</mark>');
}

function createSnippet(text, query) {
    const normalized = textOnly(text);
    if (!normalized) return '';

    const terms = getTerms(query);
    const match = findTermIndex(normalized, terms);
    const radius = 72;
    const start = Math.max(0, match.index - radius);
    const end = Math.min(normalized.length, match.index + Math.max(match.term.length, 18) + radius);
    const prefix = start > 0 ? '...' : '';
    const suffix = end < normalized.length ? '...' : '';

    return prefix + highlightText(normalized.slice(start, end), query) + suffix;
}

function pickMatchSource(result) {
    const item = result.item;
    const matches = result.matches || [];
    const contentMatch = matches.find((match) => match.key === 'content');
    const summaryMatch = matches.find((match) => match.key === 'summary');
    const titleMatch = matches.find((match) => match.key === 'title');

    if (contentMatch) return item.content;
    if (summaryMatch) return item.summary;
    if (titleMatch) return item.summary || item.content || item.title;
    return item.summary || item.content || item.title;
}

function buildTextFragmentUrl(permalink, source, query) {
    const normalized = textOnly(source);
    const terms = getTerms(query);
    const match = findTermIndex(normalized, terms);

    if (!normalized || !match.term) return permalink;

    const phrase = normalized.slice(match.index, Math.min(normalized.length, match.index + Math.max(match.term.length, 24)));
    return `${permalink}#:~:text=${encodeURIComponent(phrase)}`;
}

function renderResults(results, query) {
    if (!results.length) {
        resultsAvailable = false;
        resList.innerHTML = '';
        statusNode.textContent = '没有匹配结果';
        return;
    }

    const items = results.map((result) => {
        const item = result.item;
        const title = item.title || item.permalink;
        const source = pickMatchSource(result);
        const snippet = createSnippet(source, query);
        const href = buildTextFragmentUrl(item.permalink, source, query);

        return `<li class="post-entry">
            <a class="search-result-link" href="${escapeHtml(href)}" aria-label="${escapeHtml(title)}">
                <div class="search-result-title">${highlightText(title, query)}</div>
                <div class="search-result-text">${snippet}</div>
            </a>
        </li>`;
    }).join('');

    resList.innerHTML = items;
    resultsAvailable = true;
    first = resList.firstElementChild;
    last = resList.lastElementChild;
    statusNode.textContent = `${results.length} 个匹配结果`;
}

function runSearch() {
    const query = sInput.value.trim();

    currentElem = null;
    if (!query) {
        resultsAvailable = false;
        resList.innerHTML = '';
        statusNode.textContent = '';
        return;
    }

    if (!fuse) {
        statusNode.textContent = '搜索索引加载中...';
        return;
    }

    renderResults(fuse.search(query, { limit: resultLimit }), query);
}

function activeToggle(anchor) {
    document.querySelectorAll('.focus').forEach((element) => element.classList.remove('focus'));
    if (!anchor) return;

    anchor.focus();
    currentElem = anchor;
    anchor.parentElement.classList.add('focus');
}

function reset() {
    resultsAvailable = false;
    resList.innerHTML = '';
    statusNode.textContent = '';
    sInput.value = '';
    sInput.focus();
}

async function loadIndex() {
    try {
        const response = await fetch(new URL('../index.json', window.location.href));
        if (!response.ok) throw new Error(response.statusText);

        const data = await response.json();
        fuse = new Fuse(data, options);
        runSearch();
    } catch (error) {
        statusNode.textContent = '搜索索引加载失败';
        console.error(error);
    }
}

if (sInput && resList && statusNode) {
    loadIndex();
    sInput.addEventListener('input', runSearch);
    sInput.addEventListener('search', function () {
        if (!this.value) reset();
    });

    document.addEventListener('keydown', function (event) {
        const key = event.key;
        const active = document.activeElement;
        const inbox = document.getElementById('searchbox').contains(active);

        if (active === sInput) {
            document.querySelectorAll('.focus').forEach((element) => element.classList.remove('focus'));
        }

        if (key === 'Escape') {
            reset();
            return;
        }

        if (!resultsAvailable || !inbox) return;

        const current = currentElem || active;
        if (key === 'ArrowDown') {
            event.preventDefault();
            if (active === sInput) {
                activeToggle(first?.querySelector('.search-result-link'));
            } else if (current?.parentElement !== last) {
                activeToggle(current.parentElement.nextElementSibling.querySelector('.search-result-link'));
            }
        } else if (key === 'ArrowUp') {
            event.preventDefault();
            if (current?.parentElement === first) {
                activeToggle(sInput);
            } else if (active !== sInput) {
                activeToggle(current.parentElement.previousElementSibling.querySelector('.search-result-link'));
            }
        } else if (key === 'ArrowRight' || key === 'Enter') {
            current?.click();
        }
    });
}
