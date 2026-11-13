const siginupForm = document.getElementById("signup-form");
const errorMsg = document.getElementById("siginup-error");

// ユーザーから入力してもらった値を検証する
function checkForm(userInfo) {
    if(userInfo["login_id"].length === 0) {
        errorMsg.textContent = "IDを入力してください。";
        errorMsg.hidden = false;
        return false;
    } else if (userInfo["login_id"].length > 20) {
        errorMsg.textContent = "IDは20桁以下にしてください。";
        errorMsg.hidden = false;
        return false;
    }

    if(userInfo["password"].length < 6 || userInfo["password"].length > 15) {
        errorMsg.textContent = "パスワードは6桁以上15桁以下にしてください。";
        errorMsg.hidden = false;
        return false;
    }

    if (userInfo["user_name"].length === 0) {
        errorMsg.textContent = "ユーザー名を入力してください。";
        errorMsg.hidden = false;
        return false;
    } else if (userInfo["user_name"].length > 25) {
        errorMsg.textContent = "ユーザー名は25文字以下にしてください。";
        errorMsg.hidden = false;
        return false;
    }

    if(userInfo["email"].length === 0) {
        errorMsg.textContent = "メールを入力してください。";
        errorMsg.hidden = false;
        return false;
    }

    errorMsg.hidden = true;
    return true;
}

siginupForm.addEventListener("submit", async (e) => {
    // form 기능 무효화
    e.preventDefault();

    // 입력 받은 정보 가져오기
    const login_id = document.getElementById("signup-login-id").value.trim();
    const password = document.getElementById("signup-password").value;
    const user_name = document.getElementById("signup-user-name").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const gender = document.getElementById("signup-gender").value;
    const introduction = document.getElementById("signup-introduction").value;
    const birthday = document.getElementById("signup-birthday").value;

    const userInfo = {
        "login_id" : login_id,
        "password" : password,
        "user_name" : user_name,
        "email" : email,
        "gender" : gender,
        "introduction" : introduction,
        "birthday" : birthday
    };

    // 입력폼 체크
    if(!checkForm(userInfo)) {
        return;
    }

    // 入力に問題がない場合、apiにその値を送信する
    
    try {
        const response = await fetch("https://api.moonlog.dev/users",{
            method : "POST",
            headers : {
                "Content-Type": "application/json",
            },
            body : JSON.stringify(userInfo)
        })

        if(response.ok) {
            location.href = "../../index.html";
            return;
        }

        // レスポンス本文はJSONで読み込む。
        // 読み込みに失敗した場合はdataにnullを格納する。
        const data = await response.json().catch(() => null);

        if (typeof data?.detail === "string") {
            errorMsg.textContent = data.detail;
        } else if (response.status === 422) {
            errorMsg.textContent = "入力内容を確認してください。";
        } else {
            errorMsg.textContent = "会員登録に失敗しました。";
        }

        errorMsg.hidden = false;
        
    } catch(error) {
        console.error(error);
        errorMsg.textContent = "サーバーに接続できませんでした。"
        errorMsg.hidden = false;
    }
});