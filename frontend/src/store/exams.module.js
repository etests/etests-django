import { examService } from "@/api/exam.service";

const initialState = {
  status: {},
  items: []
};

export const exams = {
  namespaced: true,
  state: initialState,
  actions: {
    getAll({ dispatch, commit }) {
      commit("getAllRequest");
      examService.getAll().then(
        items => {
          commit("getAllSuccess", items);
        },
        error => {
          commit("getAllFailure", error);
        }
      );
    }
  },
  mutations: {
    getAllRequest(state) {
      state.status = { loading: true };
    },
    getAllSuccess(state, exams) {
      state.status = { exists: true };
      state.items = exams;
    },
    getAllFailure(state, error) {
      state.status = { error };
    }
  }
};
