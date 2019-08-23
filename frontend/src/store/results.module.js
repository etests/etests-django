import { resultService } from "@/api/result.service";

const initialState = {
  status: {},
  result: null
};

export const results = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);
      resultService.get(id).then(
        result => {
          commit("getSuccess", result);
          setTimeout(() => {
            dispatch("alert/success", "Result fetched successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, result) {
      state.status = { exists: true };
      state.result = result;
    },
    getFailure(state, error) {
      state.status = { error };
    }
  }
};
