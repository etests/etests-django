import { testService } from "@/api/test.service";

const initialState = {
  status: {},
  test: {},
  all: { items: [] }
};

export const tests = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);

      testService.get(id).then(
        test => {
          commit("getSuccess", test);
          setTimeout(() => {
            dispatch("alert/success", "Test fetched successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    create({ dispatch, commit }, data) {
      commit("createRequest", data);

      testService.create(data).then(
        data => {
          commit("createSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test created successfully!", {
              root: true
            });
            dispatch("testSeries/addTest", data, {
              root: true
            });
          });
        },
        error => {
          commit("createFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    update({ dispatch, commit }, data) {
      commit("updateRequest", data);

      testService.update(data).then(
        data => {
          commit("updateSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test updated successfully!", {
              root: true
            });
            dispatch("testSeries/addTest", data, {
              root: true
            });
          });
        },
        error => {
          commit("updateFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      testService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Test removed successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("removeFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
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
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, test) {
      state.status = {};
      state.test = test;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, tests) {
      state.all = { items: tests };
    },
    getAllFailure(state, error) {
      state.all = { error };
    },
    createRequest(state, data) {
      state.status = { creating: true };
    },
    createSuccess(state, data) {
      state.all.items.push(data);
      state.status = { created: true, test: data };
    },
    createFailure(state, error) {
      state.status = { error: error };
    },
    updateRequest(state, data) {
      state.status = { updating: true };
    },
    updateSuccess(state, data) {
      state.status = { updated: true, test: data };
    },
    updateFailure(state, error) {
      state.status = { error: error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
      state.all.items = state.all.items.filter(test => test.id !== id);
    },
    removeFailure(state, error) {
      state.status = { error: error };
    }
  }
};
