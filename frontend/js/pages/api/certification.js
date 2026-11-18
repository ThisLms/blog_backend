async function requireAuth() {
    // sessionからトークンを取り出す
    const stored_token = sessionStorage.getItem("access_token");

    // トーキンがない場合 -> ログインページに遷移する
    if(!stored_token) {
        location.href = "/pages/auth/login.html";
        return false;
    }

    // トークンがある場合
    // apiを呼び出して、トークンを検証する
    const response = await fetch("https://api.moonlog.dev/auth/me", {
        headers : {
            Authorization: `Bearer ${stored_token}`
        }
    })

    // Access tokenに問題がない場合
    if(response.ok) {
        return true;
    }

    if (response.status !== 401) {
        throw new Error(`認証状態を確認できませんでした (${response.status})`);
    }

    const data = await response.json();

    if (data.detail === "expire") {
        const response_refresh = await fetch("https://api.moonlog.dev/auth/refresh",{
            method : "POST"
            ,credentials: "include"
        });

        if(response_refresh.ok) {
            const data_refresh = await response_refresh.json();

            if (typeof data_refresh?.access_token !== "string" || !data_refresh.access_token) {
                throw new Error("アクセストークンを取得できませんでした。");
            }

            sessionStorage.setItem("access_token", data_refresh.access_token);
            sessionStorage.setItem("user_info", JSON.stringify(data_refresh.user_info));
            return true
        }

        if (response_refresh.status !== 401) {
            throw new Error(`トークンを更新できませんでした (${response_refresh.status})`);
        }

    } else if (data.detail !== "invalid" && data.detail !== "not") {
        throw new Error("認証エラーを確認できませんでした。");
    }

    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("user_info"); // 권한 정보 삭제

    alert("ログインしてください。");
    
    location.href = "/pages/auth/login.html";
    return false;
}