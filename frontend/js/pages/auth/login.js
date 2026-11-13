const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");
const logoutBtn = document.querySelector("#logout-button")

loginForm.addEventListener("submit",async function (event) {
    event.preventDefault();

    const userId = document.querySelector("#login-id").value.trim();
    const password = document.querySelector("#login-password").value;

    loginError.hidden = true;
    loginError.textContent = "";

    // 아이디나 비밀번호가 입력이 안 된 경우
    if (!userId || !password) {
        loginError.textContent = "ID又はパスワードを入力してください。";
        loginError.hidden = false;
        return;
    }

    // 입력 받은 비밀번호의 길이가 설정된 값과 다른 경우
    if(password.length < 6 || password.length > 15) {
        loginError.textContent = "パスワードは６桁以上１５桁以下で入力してください。"
        loginError.hidden = false;
        return
    }
    
    // 입력값 검증 통과

    try {
        // API에 요청
        const response = await fetch("https://api.moonlog.dev/auth/login", {
            method: "POST",
            credentials: "include", // 리프레시 토큰 저장을 위해서 필요
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                login_id: userId,
                password: password,
            }),
        });

        const data = await response.json();

        // 로그인 성공
        if (response.ok) {
            sessionStorage.setItem("access_token", data.access_token); // 토큰 저장
            location.href = "../../index.html"; // 인덱스 화면으로 이동
            return;
        }

        if (response.status === 401) {
            loginError.textContent = data.detail;
        } else {
            loginError.textContent = "ログイン処理中エラーが発生しました。";
        }

        loginError.hidden = false;

    } catch(error) {
        console.error(error);
        loginError.textContent = "サーバーに接続できませんでした。";
        loginError.hidden = false;
    }
});