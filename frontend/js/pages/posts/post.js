'use strict';

async function initPostPage() {
    // false - ログインしていない場合はログインページに遷移される
    if (!(await requireAuth())) return;

    const postWriteForm = document.querySelector('#post-write-form');
    const postWriteTitle = document.querySelector('#post-write-title');
    const postWriteTags = document.querySelector('#post-write-tags');
    const postWriteMarkdown = document.querySelector('#post-write-markdown');
    const postWriteError = document.querySelector('#post-write-error');
    const postWriteEditFields = document.querySelector('#post-write-edit-fields');
    const postWriteEditTab = document.querySelector('#post-write-edit-tab');
    const postWritePreviewTab = document.querySelector('#post-write-preview-tab');
    const postWriteEditPanel = document.querySelector('#post-write-edit-panel');
    const postWritePreviewPanel = document.querySelector('#post-write-preview-panel');
    const postWritePreviewTitle = document.querySelector('#post-write-preview-title');
    const postWritePreviewTags = document.querySelector('#post-write-preview-tags');
    const postWritePreview = document.querySelector('#post-write-preview');
    const postWriteSubmit = document.querySelector('#post-write-submit');

    function readTags() {
        const tags = new Map();

        // 半角カンマと全角カンマで区切る
        for (const value of postWriteTags.value.split(/[,，]/)) {
            const tag = value.trim();
            const key = tag.toLowerCase();

            if (tag && !tags.has(key)) {
                tags.set(key, tag);
            }
        }

        return [...tags.values()];
    }

    function showPostWriteError(message) {
        postWriteError.textContent = message;
        postWriteError.hidden = !message;
    }

    function renderPostWritePreview() {
        postWritePreviewTitle.textContent = postWriteTitle.value.trim() || '無題の投稿';
        postWritePreviewTags.replaceChildren();

        for (const tag of readTags()) {
            const chip = document.createElement('span');
            chip.className = 'post-write-preview-tag';
            chip.textContent = `#${tag}`;
            postWritePreviewTags.append(chip);
        }

        const markdown = postWriteMarkdown.value;

        if (!markdown.trim()) {
            postWritePreview.textContent = '本文が入力されていません。';
            return;
        }

        if (typeof marked === 'undefined' || typeof DOMPurify === 'undefined') {
            postWritePreview.textContent = 'プレビュー用ライブラリを読み込めませんでした。';
            return;
        }

        const html = marked.parse(markdown, { gfm: true, breaks: false, async: false });
        postWritePreview.innerHTML = DOMPurify.sanitize(html);

        for (const link of postWritePreview.querySelectorAll('a[href]')) {
            if (/^https?:\/\//i.test(link.getAttribute('href'))) {
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
            }
        }
    }

    function setPostWriteMode(mode, focusTab = false) {
        const preview = mode === 'preview';

        if (preview) {
            renderPostWritePreview();
        }

        postWriteEditFields.hidden = preview;
        postWriteEditPanel.hidden = preview;
        postWritePreviewPanel.hidden = !preview;
        postWriteEditTab.setAttribute('aria-selected', String(!preview));
        postWritePreviewTab.setAttribute('aria-selected', String(preview));
        postWriteEditTab.tabIndex = preview ? -1 : 0;
        postWritePreviewTab.tabIndex = preview ? 0 : -1;

        if (focusTab) {
            (preview ? postWritePreviewTab : postWriteEditTab).focus();
        }
    }

    function showFieldError(field, message) {
        setPostWriteMode('edit');
        showPostWriteError(message);
        field.focus();
    }

    postWriteEditTab.addEventListener('click', () => setPostWriteMode('edit'));
    postWritePreviewTab.addEventListener('click', () => setPostWriteMode('preview'));

    for (const tab of [postWriteEditTab, postWritePreviewTab]) {
        tab.addEventListener('keydown', (event) => {
            if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;

            event.preventDefault();
            setPostWriteMode(tab === postWriteEditTab ? 'preview' : 'edit', true);
        });
    }

    // indexページへ
    document.querySelector('#location-home').addEventListener('click', () => {
        location.href = '../../index.html';
    });

    // 投稿内容初期化
    document.querySelector('#post-write-clear').addEventListener('click', () => {
        postWriteForm.reset();
        showPostWriteError('');
        setPostWriteMode('edit');
        postWriteTitle.focus();
    });

    // 投稿
    postWriteForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (postWriteSubmit.disabled) return;
        
        showPostWriteError('');

        const title = postWriteTitle.value.trim();
        const content = postWriteMarkdown.value.trim();
        const tags = readTags();

        if (!title) {
            showFieldError(postWriteTitle, 'タイトルを入力してください。');
            return;
        }

        if (!content) {
            showFieldError(postWriteMarkdown, '本文を入力してください。');
            return;
        }

        if (tags.length > 5) {
            showFieldError(postWriteTags, 'タグは5個まで入力できます。');
            return;
        }

        if (tags.some((tag) => [...tag].length > 10)) {
            showFieldError(postWriteTags, '各タグは10文字以内で入力してください。');
            return;
        }
        
        // ここに投稿APIへのリクエストを追加する
        const payload = { title, content, tags };
        const accessToken = sessionStorage.getItem("access_token");

        postWriteSubmit.disabled = true;

        try {
            let response = await fetch("https://api.moonlog.dev/posts",{
                method : "POST"
                ,headers : {
                    Authorization: `Bearer ${accessToken}`
                    ,"Content-Type": "application/json"
                }
                ,body : JSON.stringify(payload)
            });
            
            // トークンの期間切れなどで現在のトークンが使えない場合
            // Access Tokenを再発行して、再確認する。
            if(response.status === 401) {

                // 再認証
                if (!(await requireAuth())) return;

                const newAccessToken = sessionStorage.getItem("access_token");

                // 再提出
                response = await fetch("https://api.moonlog.dev/posts", {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${newAccessToken}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload)
                });
            }

            if(response.ok) {
                alert("投稿が正常に登録されました。");
                location.href = "../../index.html";
                return;
            }

            showPostWriteError(`投稿に失敗しました (${response.status})。`);
        } catch (error) {
            console.error(error);
            showPostWriteError("投稿を完了できませんでした。もう一度お試しください。");
        } finally {
            postWriteSubmit.disabled = false;
        }
    });

    postWriteForm.hidden = false;
}

initPostPage().catch((error) => {
    console.error(error);

    const errorMessage = document.querySelector('#post-write-auth-error');
    errorMessage.textContent = '認証状態を確認できませんでした。ページを再読み込みしてください。';
    errorMessage.hidden = false;
});