import streamlit as st
import requests
import time
import json 

# initialize app session data
if "init" not in st.session_state:
    print("init....")
    st.session_state["init"] = True
    st.session_state["llama_response"] = None
    st.session_state["llama_response_time"] = None


def query_llama():
    prompt = st.session_state.llama_prompt
    st.session_state["llama_response"] = None
    st.session_state["llama_response_time"] = None
    url = "http://34.133.124.59:8080/v1/models/model:predict"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    start_time = time.time()
    print("sending prediction request...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=180)
        # Record the end time
        end_time = time.time()

        # Calculate the time taken
        time_taken = end_time - start_time

        # Print the response and time taken
        parsed_data = json.loads(response.text)
        st.session_state["llama_response"] = parsed_data['data']['generated_text']
        st.session_state["llama_response_time"] = time_taken
        print(f"Time taken to get the response: {time_taken:.2f} seconds")
    except Exception as e:
        print("failed to get a response")


def main():
    st.text_input("Ask Llama Anything", key="llama_prompt")
    st.button("Submit", on_click=query_llama)
    if st.session_state["llama_response"]:
        st.write(st.session_state["llama_response"])
        st.write(f"Time taken: {st.session_state['llama_response_time']:.2f} seconds")


if __name__ == "__main__":
    main()
