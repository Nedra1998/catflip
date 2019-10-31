#!/usr/bin/python3

import numpy as np
from argparse import ArgumentParser
import xml.etree.ElementTree as ET

def add_cylinder(base, length, radius):
    geometry = ET.SubElement(base, 'geometry')
    cylinder = ET.SubElement(geometry, 'cylinder')
    cylinder.set('length', str(length))
    cylinder.set('radius', str(radius))

def add_sphere(base, radius):
    geometry = ET.SubElement(base, 'geometry')
    cylinder = ET.SubElement(geometry, 'sphere')
    cylinder.set('radius', str(radius))

def add_origin(base, rx, ry, rz, tx, ty, tz):
    origin = ET.SubElement(base, 'origin')
    origin.set('rpy', "{} {} {}".format(rx, ry, rz))
    origin.set('xyz', "{} {} {}".format(tx,ty,tz))

def add_material(base, r, g, b, a):
    material = ET.SubElement(base, 'material')
    material.set('name', "gen-mat")
    color = ET.SubElement(material, 'color')
    color.set('rgba', "{} {} {} {}".format(1.0, 1.0, 1.0,a))

def add_legs(root, body, len, rad, rx, ry, rz, tx, ty, tz):
    leg = ET.SubElement(root, 'link')
    leg.set('name', "{}-leg".format(body))
    visual = ET.SubElement(leg, 'visual')
    add_cylinder(visual, 0.5, 0.1)
    add_material(visual, 1.0, 1.0, 1.0, 1.0)
    add_origin(visual, 0.0,0.0, 0.0, tx, ty, tz + rad / 2.0)
    joint = ET.SubElement(root, 'joint')
    joint.set('name', '{}-leg-to-{}'.format(body, body))
    joint.set('type', 'fixed')
    parent = ET.SubElement(joint, 'parent')
    parent.set('link', body)
    child = ET.SubElement(joint, 'child')
    child.set('link', '{}-leg'.format(body))
    origin = ET.SubElement(joint, 'origin')
    origin.set("xyz", "{} {} {}".format(tx, ty, tz + rad/2.0))

    # vc.set('name', 'vec_to_center')
    # vc.set('type', 'fixed')
    # parent = ET.SubElement(vc, 'parent')
    # parent.set('link', body)
    # child = ET.SubElement(vc, 'child')
    # child.set('link', 'leg{}'.format(name))
    # origin = ET.SubElement(vc, "origin")
    # origin.set("xyz", "0 0 0")




def main():
    parser = ArgumentParser()
    parser.add_argument('-fl', '--flength', default=1.0, type=float, help="Length of front body")
    parser.add_argument('-fc','--fcone', default=0.3, type=float, help="Length of front cone")
    parser.add_argument('-fr','--fradius', default=0.2, type=float, help="Radius of front body")
    parser.add_argument('-fm','--fmass', default=5.0, type=float, help="Mass of front body")
    parser.add_argument('-fmc','--fmasscone', default=0.0, type=float, help="Mass of front cone")
    parser.add_argument('-bl','--blength', default=1.0, type=float, help="Length of back body")
    parser.add_argument('-bc','--bcone', default=0.3, type=float, help="Length of back cone")
    parser.add_argument('-br','--bradius', default=0.2, type=float, help="Radius of back body")
    parser.add_argument('-bm','--bmass', default=5.0, type=float, help="Mass of back body")
    parser.add_argument('-bmc','--bmasscone', default=0.0, type=float, help="Mass of back cone")
    parser.add_argument('-cr','--cradius', default=0.1, type=float, help="Radius of center sphere")
    parser.add_argument('-cm','--cmass', default=0.0, type=float, help="Mass of center sphere")
    parser.add_argument('-a','--alpha', default=np.pi, type=float, help="Inital bend of the cat")

    args = parser.parse_args()

    robot = ET.Element('robot')
    robot.set('name', 'robocat')

    phi = (np.pi - args.alpha) / 2.0
    frx, fry, frz = -args.alpha / 2.0, 0.0, 0.0
    ftx, fty, ftz = 0.0, args.flength/2.0*np.cos(phi) + args.cradius, args.flength/2.0 * np.sin(phi)

    front_cylinder = ET.SubElement(robot, 'link')
    front_cylinder.set('name', 'frontCylinder')
    visual = ET.SubElement(front_cylinder, 'visual')
    add_cylinder(visual, args.flength, args.fradius)
    add_origin(visual, frx,fry,frz,ftx,fty,ftz)
    add_material(visual, 1.0, 1.0, 0.0, 1.0)
    collision = ET.SubElement(front_cylinder, 'collision')
    add_cylinder(collision, args.flength, args.fradius)
    add_origin(collision, frx,fry,frz,ftx,fty,ftz)
    inertial = ET.SubElement(front_cylinder, 'inertial')
    mass = ET.SubElement(inertial, 'mass')
    mass.set('value', "{}".format(args.fmass))
    intertia = ET.SubElement(inertial, 'inertia')
    intertia.set('ixx', str(1/4*args.fmass*args.fradius**2+1/12*args.fmass*args.flength**2))
    intertia.set('iyy', str(1/4*args.fmass*args.fradius**2+1/12*args.fmass*args.flength**2))
    intertia.set('izz', str(1/2*args.fmass*args.fradius**2))
    intertia.set('ixy', "0.0")
    intertia.set('ixz', "0.0")
    intertia.set('iyz', "0.0")
    add_origin(inertial, frx,fry,frz,ftx,fty,ftz)
    add_legs(robot, 'frontCylinder', args.flength, args.fradius, frx, fry, frz, ftx, fty, ftz)

    brx, bry, brz = args.alpha / 2.0, 0.0, 0.0
    btx, bty, btz = 0.0, -args.blength/2.0*np.cos(phi) - args.cradius, args.flength/2.0 * np.sin(phi)

    back_cylinder = ET.SubElement(robot, 'link')
    back_cylinder.set('name', 'backCylinder')
    visual = ET.SubElement(back_cylinder, 'visual')
    add_cylinder(visual, args.blength, args.bradius)
    add_origin(visual, brx,bry,brz,btx,bty,btz)
    add_material(visual, 0.0, 1.0, 0.0, 1.0)
    collision = ET.SubElement(back_cylinder, 'collision')
    add_cylinder(collision, args.blength, args.bradius)
    add_origin(collision, brx,bry,brz,btx,bty,btz)
    inertial = ET.SubElement(back_cylinder, 'inertial')
    mass = ET.SubElement(inertial, 'mass')
    mass.set('value', "{}".format(args.bmass))
    intertia = ET.SubElement(inertial, 'inertia')
    intertia.set('ixx', str(1/4*args.bmass*args.bradius**2+1/12*args.bmass*args.blength**2))
    intertia.set('iyy', str(1/4*args.bmass*args.bradius**2+1/12*args.bmass*args.blength**2))
    intertia.set('izz', str(1/2*args.bmass*args.bradius**2))
    intertia.set('ixy', "0.0")
    intertia.set('ixz', "0.0")
    intertia.set('iyz', "0.0")
    add_origin(inertial, brx,bry,brz,btx,bty,btz)
    add_legs(robot, 'backCylinder', args.blength, args.bradius, brx, bry, brz, btx, bty, btz)

    center = ET.SubElement(robot, 'link')
    center.set('name', 'centerSphere')
    visual = ET.SubElement(center, 'visual')
    add_sphere(visual, args.cradius)
    add_material(visual, 1.0, 0.0, 0.0, 1.0)
    add_origin(visual, 0.0, 0.0, 0.0, 0.0, 0.0,0.0)

    fc = ET.SubElement(robot, 'joint')
    fc.set('name', 'front_to_center')
    fc.set('type', 'revolute')
    axis = ET.SubElement(fc, 'axis')
    axis.set("xyz", "1 0 0")
    limit = ET.SubElement(fc, 'limit')
    limit.set("effort", "0.0")
    limit.set("lower", "-1.507")
    limit.set("upper", "1.507")
    limit.set("velocity", "0.5")
    parent = ET.SubElement(fc, 'parent')
    parent.set('link', 'centerSphere')
    child = ET.SubElement(fc, 'child')
    child.set('link', 'frontCylinder')
    origin = ET.SubElement(fc, "origin")
    origin.set("xyz", "0 0 0")

    bc = ET.SubElement(robot, 'joint')
    bc.set('name', 'back_to_center')
    bc.set('type', 'revolute')
    axis = ET.SubElement(bc, 'axis')
    axis.set("xyz", "0 0 1")
    limit = ET.SubElement(bc, 'limit')
    limit.set("effort", "0.0")
    limit.set("lower", "-1.507")
    limit.set("upper", "1.507")
    limit.set("velocity", "0.5")
    parent = ET.SubElement(bc, 'parent')
    parent.set('link', 'centerSphere')
    child = ET.SubElement(bc, 'child')
    child.set('link', 'backCylinder')
    origin = ET.SubElement(bc, "origin")
    origin.set("xyz", "0 0 0")

    out = open("robocat.urdf", 'w')
    out.write("<?xml version=\"1.0\"?>")
    out.write(ET.tostring(robot).decode('utf-8'))

if __name__ == "__main__":
    main()
