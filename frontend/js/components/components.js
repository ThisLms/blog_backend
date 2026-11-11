// 헤더 삽입
fetch("/components/header.html")
    .then((response) => response.text())
    .then((data) => {
        const headerHtml = document.getElementById("header");
        headerHtml.innerHTML = data;

        const token = sessionStorage.getItem("access_token");
        const loginBefore = document.getElementById("login-before-user");
        const loginAfter = document.getElementById("login-after-user");

        if (token) {
            loginBefore.hidden = true;
            loginAfter.hidden = false;
        }
    })
    .catch((error) => console.log(error));

// 로그아웃 버튼 클릭시
document.getElementById("logout-button").addEventListener("click",(e) => {
    sessionStorage.removeItem("access_token");
});

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