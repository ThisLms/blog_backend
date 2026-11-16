// 헤더 삽입
fetch("/components/header.html")
    .then((response) => response.text())
    .then((data) => {
        const headerHtml = document.getElementById("header");
        headerHtml.innerHTML = data;

        // 로그아웃 처리
        const logoutBtn = document.querySelector("#logout-button");

        logoutBtn.addEventListener("click", async () => {
            logoutBtn.disabled = true;

            try {
                const response = await fetch("https://api.moonlog.dev/auth/logout", {
                    method : "POST"
                    ,credentials : "include"
                })

                // ログアウトに失敗した際
                if(!response.ok) {
                    throw new Error(`ログアウトに失敗(${response.status})`);
                }

                // ログアウトに成功した際
                sessionStorage.removeItem("access_token"); // 토큰 삭제
                sessionStorage.removeItem("user_info"); // 권한 정보 삭제
                location.href = "/index.html";
            } catch(error) {
                console.error(error);
                alert("ログアウトに失敗しました。もう一度試してください。");
                logoutBtn.disabled = false;
            }
        });

        const token = sessionStorage.getItem("access_token");
        const loginBefore = document.getElementById("login-before-user");
        const loginAfter = document.getElementById("login-after-user");
        const userName = document.getElementById("user-name");

        if (token) {
            loginBefore.hidden = true;
            loginAfter.hidden = false;

            const storedUserInfo = sessionStorage.getItem("user_info");
            const userInfo = storedUserInfo ? JSON.parse(storedUserInfo) : null;

            if (userInfo?.user_name) {
                userName.textContent = `こんにちは、${userInfo.user_name}さん`;
                userName.hidden = false;
            }
        }
    })
    .catch((error) => console.log(error));

// 사이드바 삽입
fetch("/components/sidebar.html")
    .then((response) => response.text())
    .then((data) => {
        const sidebarHtml = document.getElementById("sidebar");

        sidebarHtml.innerHTML = data;
    })
    .catch((error) => console.log(error));

// 푸터 삽입
fetch("/components/footer.html")
    .then((response) => response.text())
    .then((data) => {
        const footerHtml = document.getElementById("footer");

        footerHtml.innerHTML = data;
    })
    .catch((error) => console.log(error));