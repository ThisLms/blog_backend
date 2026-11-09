const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");

loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const userId = document.querySelector("#login-id").value.trim();
    const password = document.querySelector("#login-password").value;

    loginError.hidden = true;
    loginError.textContent = "";

    // 아이디나 비밀번호가 입력이 안 된 경우
    if (!userId || !password) {
        loginError.textContent = "아이디와 비밀번호를 입력해 주세요.";
        loginError.hidden = false;
        return;
    }

    // 입력 받은 비밀번호의 길이가 설정된 값과 다른 경우
    if(password.length < 6 || password.length > 15) {
        loginError.textContent = "비밀번호는 6 자리이상 15 이하입니다."
        loginError.hidden = false;
        return
    }

    // 로그인 성공 후
    loginError.hidden = true;
    const userid = document.getElementById("login-id").value
    const userpw = document.getElementById("login-password").value

    fetch("https://api.moonlog.dev/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: userid,
            password: userpw,
        }),
    })
    .then(async (response) => {
        if (response.ok) {
            location.href = "../../index.html";
        } else {
            console.error(response.status, await response.json());

            loginError.textContent =
                response.status === 401
                    ? "아이디 또는 비밀번호가 일치하지 않습니다."
                    : "로그인 요청을 처리하지 못했습니다.";

            loginError.hidden = false;
        }
    })
    .catch((error) => {
        console.error(error);
        loginError.textContent = "서버에 연결하지 못했습니다.";
        loginError.hidden = false;
    });
});