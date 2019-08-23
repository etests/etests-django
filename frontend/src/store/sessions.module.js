import { sessionService } from "@/api/session.service";

const session = JSON.parse(localStorage.getItem("session"));
const initialState = session
  ? {
      status: { exists: true },
      session,
      all: { items: [] }
    }
  : {
      status: {},
      session: null,
      all: { items: [] }
    };

export const sessions = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);
      sessionService.get(id).then(
        session => {
          commit("getSuccess", session);
          setTimeout(() => {
            dispatch("alert/success", "Session fetched successfully!", {
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
    update({ dispatch, commit }, data) {
      commit("updateRequest", data);

      sessionService.update(data).then(
        data => {
          commit("updateSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Session updated successfully!", {
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

      sessionService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Session removed successfully!", {
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

      sessionService
        .getAll()
        .then(
          sessions => commit("getAllSuccess", sessions),
          error => commit("getAllFailure", error)
        );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, session) {
      state.status = { exists: true };
      state.session = session;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, sessions) {
      state.all = { items: sessions };
    },
    getAllFailure(state, error) {
      state.all = { error };
    },
    updateRequest(state, data) {
      state.status = { creating: true };
    },
    updateSuccess(state, data) {
      state.status = { created: true, session: data };
    },
    updateFailure(state, error) {
      state.status = { error: error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
    },
    removeFailure(state, error) {
      state.status = { error: error };
    }
  }
};
