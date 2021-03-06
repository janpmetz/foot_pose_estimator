#include "tensorflow/core/public/session.h"
#include "tensorflow/core/platform/env.h"
#include "multi_contact_point_model_run_lib.h"

//#include <limits.h>
//#include <unistd.h>

#include <cmath>

using namespace tensorflow;

MultiContactPointModel::MultiContactPointModel() {
}

MultiContactPointModel::~MultiContactPointModel() {
}

// takes a while bc loads the graph, preferably only load it once
void MultiContactPointModel::init(std::string modelPath) {
	
  // Initialize a tensorflow session
  //Session* session;
  Status status = NewSession(SessionOptions(), &session);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
  }

  // Read in the protobuf graph we exported
  // (The path seems to be relative to the cwd. Keep this in mind
  // when using `bazel run` since the cwd isn't where you call
  // `bazel run` but from inside a temp folder.)
  GraphDef graph_def;

  status = ReadBinaryProto(Env::Default(), modelPath, &graph_def); // "/home/jan/IP/frozen_model.pb"
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
  }

  // Add the graph to the session
  status = session->Create(graph_def);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
  }
}


// model path for frozen model (including weights) with filename
std::vector<double> MultiContactPointModel::make_prediction(std::vector<double> pointsFlat, std::vector<double> zmpvec, int dataWidth, int dataHeight) {

  std::vector<double> pred;

  // for matrix shaped input to nn
  int length = dataWidth*dataHeight;
  Tensor X(DT_FLOAT, TensorShape({1,length}));
  auto mat = X.tensor<float, 2>();
  for(int i = 0; i < length; i++) {
	    mat(0, i) = (float)pointsFlat.at(i);
  }

  std::vector<std::pair<string, tensorflow::Tensor>> inputs = {
    { "X", X }
  };

  // The session will initialize the outputs
  std::vector<tensorflow::Tensor> outputs;

  // Run the session, evaluating our "c" operation from the graph
  Status status = session->Run(inputs, {"myypred"}, {}, &outputs);
  if (!status.ok()) {
    std::cout << "in loader.cc (tensorflow pred model) failed: "<< status.ToString() << "\n";
    return pred;
  }

  auto output_mat = outputs[0].matrix<float>(); // TODO maybe possible to get the flat vector directly

  for(int i = 0; i < dataHeight; i++) {
    for(int j = 0; j < dataWidth; j++) {
      auto out_elem = output_mat(0, (i*dataWidth)+j);
      pred.push_back((double)out_elem);
    }
  }

  // There are similar methods for vectors and matrices here:
  // https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/public/tensor.h)

  return pred;
}

// Free any resources used by the session
void MultiContactPointModel::close() {
  session->Close();
}
