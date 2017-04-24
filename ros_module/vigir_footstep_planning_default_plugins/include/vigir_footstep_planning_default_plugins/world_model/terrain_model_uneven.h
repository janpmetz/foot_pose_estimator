//=================================================================================================
// Copyright (c) 2016, Alexander Stumpf, TU Darmstadt
// All rights reserved.

// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//     * Neither the name of the Simulation, Systems Optimization and Robotics
//       group, TU Darmstadt nor the names of its contributors may be used to
//       endorse or promote products derived from this software without
//       specific prior written permission.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//=================================================================================================

#ifndef VIGIR_FOOTSTEP_PLANNING_TERRAIN_MODEL_UNEVEN_H__
#define VIGIR_FOOTSTEP_PLANNING_TERRAIN_MODEL_UNEVEN_H__

#include <ros/ros.h>

#include <boost/thread/mutex.hpp>

#include <pcl/point_cloud.h>

#include <vigir_footstep_planning_lib/modeling/state.h>

#include <vigir_footstep_planning_plugins/plugins/terrain_model_plugin.h>

#include <vigir_terrain_classifier/terrain_model.h>
#include <vigir_footstep_planning_default_plugins/world_model/terrain_model.h>

//#include "my_tensorflow_model_run_lib.h"
#include <vigir_footstep_planning_default_plugins/uneven_terrain_stand/my_tensorflow_model_run_lib.h>

namespace vigir_footstep_planning
{
class TerrainModelUneven
  : public TerrainModel
{
public:
	TerrainModelUneven(const std::string& name = "terrain_model");

  bool update3DData(geometry_msgs::Pose& p) const override;
  bool update3DData(State& s) const override;

  // typedefs
  typedef boost::shared_ptr<TerrainModelUneven> Ptr;
  typedef boost::shared_ptr<TerrainModelUneven> ConstPtr;

protected:
  // ml model for foot on terrain
  MyPredict* myPred;
};
}

#endif
