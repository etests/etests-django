import { testService } from "@/api/test.service";

export const tests = {
  namespaced: true,
  state: {
    all: {}
  },
  actions: {
    getAll({ commit }) {
      commit("getAllRequest");

      testService
        .getAll()
        .then(
          tests => commit("getAllSuccess", tests),
          error => commit("getAllFailure", error)
        );
    }
  },
  mutations: {
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, tests) {
      state.all = { items: tests };
    },
    getAllFailure(state, error) {
      state.all = { error };
    }
  }
};
