from app.repositories.post_repository import transaction,save_post,search_tag,save_tag,connect_post_tag

def service_post_register(data,user_id):
    # 입력 받은 값 검사
    if data.title.strip() == "" or data.content.strip() == "":
        return {
            "error_code" : "E015"
            ,"flag" : False
        }

    tags = [tag.strip() for tag in data.tags]
    tags = [tag for tag in tags if tag]

    for tag in tags:
        if len(tag) > 10:
            return {
                "error_code": "E015",
                "flag": False,
            }

    # 트랜젝션 시작
    with transaction() as conn:
        # 1. 댓글 저장
        post_id = save_post(conn,data,user_id)

        # 2. 태그 저장 (검색 후 태그가 존재하면 그 태그 사용)
        ## 2_1 태그 검색
        id_tags = []

        for tag in tags:
            # 태그 수만큼 반복하면서 검색
            result = search_tag(conn,tag)

            if result is not None :
                # 반환 받은 태그 아이디를 태그 아이디 배열에 저장
                id_tags.append(result["tag_id"])
            else :
                # 중복되는 태그가 없는 경우에는 태그 새로 등록 후 배열에 저장
                tag_id = save_tag(conn,tag)
                id_tags.append(tag_id)

        # 3. 게시글 - 태그 연결
        for tag in set(id_tags):
            connect_post_tag(conn,post_id,tag)

    return {
        "post_id" : post_id
        ,"flag" : True
    }