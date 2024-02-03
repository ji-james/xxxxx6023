import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc



# Data Viz Pkgs
import plotly.express as px 


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">연산역 할일매뉴얼</h1>
    <p style="color:white;text-align:center;">2024.02.02</p>
    </div>
    """


def main():
	stc.html(HTML_BANNER)


	menu = ["작성하기","보기","추가","삭제","기타"]
	choice = st.sidebar.selectbox("목차",menu)
	create_table()

	if choice == "작성하기":
		st.subheader("항목 추가")
		leftcolumn,rightcolumn = st.columns(2)
		
		with leftcolumn:
			task = st.text_area("업무 내용")

		with rightcolumn:
			task_status = st.selectbox("작성내용",["할일","한일","끝낸일"])
			task_due_date = st.date_input("날짜")

		if st.button("추가버튼"):
			add_data(task,task_status,task_due_date)
			st.success("Added ::{} ::To Task".format(task))


	elif choice == "보기":
		# st.subheader("View Items")
		with st.expander("작성내용"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["내용","상태","날짜"])
			# clean_df = clean_df.astype(bool)
			st.dataframe(clean_df)

		with st.expander("통계그래프"):
			task_df = clean_df['상태'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='상태',values='count')
			st.plotly_chart(p1,use_container_width=True)


	elif choice == "추가":
		st.subheader("내용추가")
		with st.expander("적힌 내용"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["내용","상태","날짜"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("내용",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			leftcolumn,rightcolumn = st.columns(2)
			
			with leftcolumn:
				new_task = st.text_area("적힌 내용",task)

			with rightcolumn:
				new_task_status = st.selectbox(task_status,["내용","상태","날짜"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("내용추가"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.expander("새로고친 내용"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["내용","상태","날짜"])
				st.dataframe(clean_df)


	elif choice == "삭제":
		st.subheader("삭제하기")
		with st.expander("적힌 내용"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["내용","상태","날짜"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("선택내용",unique_list)
		if st.button("삭제"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("삭제후 내용"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["내용","상태","날짜"])
			st.dataframe(clean_df)

	else:
		st.subheader("기타")
		st.info("불편한 점이 있으시면")
		st.info("kim1405 @humetro.busan.kr")
		st.text("문의해 주세요")


if __name__ == '__main__':
	main()