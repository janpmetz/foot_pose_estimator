/*
 * DataPoints.cpp
 *
 *  Created on: Nov 21, 2016
 *      Author: jan
 */

#include <cmath>
#include <vigir_footstep_planning_default_plugins/uneven_terrain_stand/data_points.h>


DataPoints::DataPoints(std::vector<orgQhull::vec3> points)
: points(points)
{

}

DataPoints::~DataPoints() {
}

std::vector<orgQhull::vec3> DataPoints::getPoints() {
	return points;
}
