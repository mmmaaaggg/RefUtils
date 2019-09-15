#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/8/16 9:37
@File    : load_xml_str_demo.py
@contact : mmmaaaggg@163.com
@desc    : 通过xml string的方式加载 bpmn 对象
How to install bpmn-python?
cd C:\GitHub\bpmn-python
python setup.py sdist bdist_wheel
pip install C:\GitHub\bpmn-python\dist\bpmn_python-0.0.19_SNAPSHOT-py3-none-any.whl
"""

import io

import bpmn_python.bpmn_diagram_rep as diagram

graph = diagram.BpmnDiagramGraph()
assert graph.bpmndi_namespace == 'bpmndi:'
assert graph.collaboration == {}
assert graph.diagram_attributes == {}
assert graph.plane_attributes == {}
assert graph.process_elements == {}
assert graph.sequence_flows == {}
assert graph.diagram_graph.adj == {}
assert graph.diagram_graph.edge == {}
assert graph.diagram_graph.graph == {}
assert graph.diagram_graph.node == {}
assert graph.diagram_graph.name == ''

xml_str = \
    '<?xml version="1.0" encoding="UTF-8"?>\n' \
    '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"' \
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"' \
    ' xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC" xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI"' \
    ' xmlns:activiti="http://activiti.org/bpmn" xmlns:xsd="http://www.w3.org/2001/XMLSchema"' \
    ' targetNamespace="http://www.activiti.org/test">\n' \
    '  <process id="leave" name="My process" isExecutable="true">\n' \
    '    <userTask id="deptleaderaudit" name="部门经理审批" activiti:candidateGroups="部门经理" />\n' \
    '    <exclusiveGateway id="exclusivegateway1" />\n' \
    '    <userTask id="hraudit" name="人事审批" activiti:candidateGroups="人事" />\n' \
    '    <sequenceFlow id="flow3" name="同意" sourceRef="exclusivegateway1" targetRef="hraudit">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${approve==\'true\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <userTask id="modifyapply" name="调整申请" activiti:assignee="${applyuserid}" />\n' \
    '    <sequenceFlow id="flow4" name="拒绝" sourceRef="exclusivegateway1" targetRef="modifyapply">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${approve==\'false\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <sequenceFlow id="flow6" sourceRef="deptleaderaudit" targetRef="exclusivegateway1" />\n' \
    '    <exclusiveGateway id="exclusivegateway2">\n' \
    '      <outgoing>SequenceFlow_19ph05v</outgoing>\n' \
    '    </exclusiveGateway>\n' \
    '    <sequenceFlow id="flow7" sourceRef="modifyapply" targetRef="exclusivegateway2" />\n' \
    '    <sequenceFlow id="flow8" name="重新申请" sourceRef="exclusivegateway2" targetRef="deptleaderaudit">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${reapply==\'true\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <exclusiveGateway id="exclusivegateway3" />\n' \
    '    <sequenceFlow id="flow10" sourceRef="hraudit" targetRef="exclusivegateway3" />\n' \
    '    <sequenceFlow id="flow11" name="拒绝" sourceRef="exclusivegateway3" targetRef="modifyapply">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${approve==\'false\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <userTask id="reportback" name="销假" activiti:assignee="${applyuserid}">\n' \
    '      <outgoing>SequenceFlow_0o99twi</outgoing>\n' \
    '    </userTask>\n' \
    '    <startEvent id="startevent1" activiti:initiator="${applyuserid}" />\n' \
    '    <sequenceFlow id="flow14" sourceRef="startevent1" targetRef="deptleaderaudit" />\n' \
    '    <userTask id="usertask1" name="人事审核" />\n' \
    '    <sequenceFlow id="flow17" sourceRef="exclusivegateway1" targetRef="usertask1">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${approve==\'true\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <sequenceFlow id="flow18" name="同意" sourceRef="exclusivegateway3" targetRef="reportback">\n' \
    '      <conditionExpression xsi:type="tFormalExpression">${approve==\'true\'}</conditionExpression>\n' \
    '    </sequenceFlow>\n' \
    '    <endEvent id="EndEvent_0ls7use">\n' \
    '      <incoming>SequenceFlow_19ph05v</incoming>\n' \
    '      <incoming>SequenceFlow_0o99twi</incoming>\n' \
    '    </endEvent>\n' \
    '    <sequenceFlow id="SequenceFlow_19ph05v" sourceRef="exclusivegateway2" targetRef="EndEvent_0ls7use" />\n' \
    '    <sequenceFlow id="SequenceFlow_0o99twi" sourceRef="reportback" targetRef="EndEvent_0ls7use" />\n' \
    '  </process>\n' \
    '  <bpmndi:BPMNDiagram id="BPMNDiagram_leave">\n' \
    '    <bpmndi:BPMNPlane id="BPMNPlane_leave" bpmnElement="leave">\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_deptleaderaudit" bpmnElement="deptleaderaudit">\n' \
    '        <omgdc:Bounds x="150" y="222" width="105" height="55" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_exclusivegateway1" bpmnElement="exclusivegateway1" isMarkerVisible="true">\n' \
    '        <omgdc:Bounds x="435" y="229" width="40" height="40" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_hraudit" bpmnElement="hraudit">\n' \
    '        <omgdc:Bounds x="557" y="222" width="105" height="55" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_modifyapply" bpmnElement="modifyapply">\n' \
    '        <omgdc:Bounds x="403" y="312" width="105" height="55" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_exclusivegateway2" bpmnElement="exclusivegateway2" isMarkerVisible="true">\n' \
    '        <omgdc:Bounds x="435" y="412" width="40" height="40" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_exclusivegateway3" bpmnElement="exclusivegateway3" isMarkerVisible="true">\n' \
    '        <omgdc:Bounds x="707" y="230" width="40" height="40" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_reportback" bpmnElement="reportback">\n' \
    '        <omgdc:Bounds x="859" y="223" width="105" height="55" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_startevent1" bpmnElement="startevent1">\n' \
    '        <omgdc:Bounds x="40" y="232" width="35" height="35" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNShape id="BPMNShape_usertask1" bpmnElement="usertask1">\n' \
    '        <omgdc:Bounds x="557" y="222" width="105" height="55" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow3" bpmnElement="flow3">\n' \
    '        <omgdi:waypoint x="475" y="249" />\n' \
    '        <omgdi:waypoint x="557" y="249" />\n' \
    '        <bpmndi:BPMNLabel>\n' \
    '          <omgdc:Bounds x="486" y="249" width="23" height="14" />\n' \
    '        </bpmndi:BPMNLabel>\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow4" bpmnElement="flow4">\n' \
    '        <omgdi:waypoint x="455" y="269" />\n' \
    '        <omgdi:waypoint x="455" y="312" />\n' \
    '        <bpmndi:BPMNLabel>\n' \
    '          <omgdc:Bounds x="462" y="280" width="23" height="14" />\n' \
    '        </bpmndi:BPMNLabel>\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow6" bpmnElement="flow6">\n' \
    '        <omgdi:waypoint x="255" y="249" />\n' \
    '        <omgdi:waypoint x="435" y="249" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow7" bpmnElement="flow7">\n' \
    '        <omgdi:waypoint x="455" y="367" />\n' \
    '        <omgdi:waypoint x="455" y="412" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow8" bpmnElement="flow8">\n' \
    '        <omgdi:waypoint x="435" y="432" />\n' \
    '        <omgdi:waypoint x="202" y="431" />\n' \
    '        <omgdi:waypoint x="202" y="277" />\n' \
    '        <bpmndi:BPMNLabel>\n' \
    '          <omgdc:Bounds x="261" y="440" width="48" height="14" />\n' \
    '        </bpmndi:BPMNLabel>\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow10" bpmnElement="flow10">\n' \
    '        <omgdi:waypoint x="662" y="249" />\n' \
    '        <omgdi:waypoint x="707" y="250" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow11" bpmnElement="flow11">\n' \
    '        <omgdi:waypoint x="727" y="270" />\n' \
    '        <omgdi:waypoint x="727" y="339" />\n' \
    '        <omgdi:waypoint x="508" y="339" />\n' \
    '        <bpmndi:BPMNLabel>\n' \
    '          <omgdc:Bounds x="635" y="321" width="23" height="14" />\n' \
    '        </bpmndi:BPMNLabel>\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow14" bpmnElement="flow14">\n' \
    '        <omgdi:waypoint x="75" y="249" />\n' \
    '        <omgdi:waypoint x="150" y="249" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow17" bpmnElement="flow17">\n' \
    '        <omgdi:waypoint x="475" y="249" />\n' \
    '        <omgdi:waypoint x="557" y="249" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="BPMNEdge_flow18" bpmnElement="flow18">\n' \
    '        <omgdi:waypoint x="747" y="250" />\n' \
    '        <omgdi:waypoint x="859" y="250" />\n' \
    '        <bpmndi:BPMNLabel>\n' \
    '          <omgdc:Bounds x="785" y="249" width="23" height="14" />\n' \
    '        </bpmndi:BPMNLabel>\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNShape id="EndEvent_0ls7use_di" bpmnElement="EndEvent_0ls7use">\n' \
    '        <omgdc:Bounds x="894" y="414" width="36" height="36" />\n' \
    '      </bpmndi:BPMNShape>\n' \
    '      <bpmndi:BPMNEdge id="SequenceFlow_19ph05v_di" bpmnElement="SequenceFlow_19ph05v">\n' \
    '        <omgdi:waypoint x="475" y="432" />\n' \
    '        <omgdi:waypoint x="894" y="432" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '      <bpmndi:BPMNEdge id="SequenceFlow_0o99twi_di" bpmnElement="SequenceFlow_0o99twi">\n' \
    '        <omgdi:waypoint x="912" y="278" />\n' \
    '        <omgdi:waypoint x="912" y="414" />\n' \
    '      </bpmndi:BPMNEdge>\n' \
    '    </bpmndi:BPMNPlane>\n' \
    '  </bpmndi:BPMNDiagram>\n' \
    '</definitions>\n'

xml_stream = io.StringIO(xml_str)
graph.load_diagram_from_xml_file(xml_stream)
assert graph.diagram_attributes == {'id': 'BPMNDiagram_leave', 'name': ''}
assert graph.plane_attributes == {'id': 'BPMNPlane_leave', 'bpmnElement': 'leave'}
assert graph.process_elements == {
    'leave': {'id': 'leave', 'name': 'My process', 'isClosed': 'false', 'isExecutable': 'true', 'processType': 'None',
              'node_ids': ['deptleaderaudit', 'exclusivegateway1', 'hraudit', 'modifyapply', 'exclusivegateway2',
                           'exclusivegateway3', 'reportback', 'startevent1', 'usertask1', 'EndEvent_0ls7use']}}
assert graph.sequence_flows == {
    'flow3': {'name': '同意', 'sourceRef': 'exclusivegateway1', 'targetRef': 'hraudit'},
    'flow4': {'name': '拒绝', 'sourceRef': 'exclusivegateway1', 'targetRef': 'modifyapply'},
    'flow6': {'name': '', 'sourceRef': 'deptleaderaudit', 'targetRef': 'exclusivegateway1'},
    'flow7': {'name': '', 'sourceRef': 'modifyapply', 'targetRef': 'exclusivegateway2'},
    'flow8': {'name': '重新申请', 'sourceRef': 'exclusivegateway2', 'targetRef': 'deptleaderaudit'},
    'flow10': {'name': '', 'sourceRef': 'hraudit', 'targetRef': 'exclusivegateway3'},
    'flow11': {'name': '拒绝', 'sourceRef': 'exclusivegateway3', 'targetRef': 'modifyapply'},
    'flow14': {'name': '', 'sourceRef': 'startevent1', 'targetRef': 'deptleaderaudit'},
    'flow17': {'name': '', 'sourceRef': 'exclusivegateway1', 'targetRef': 'usertask1'},
    'flow18': {'name': '同意', 'sourceRef': 'exclusivegateway3', 'targetRef': 'reportback'},
    'SequenceFlow_19ph05v': {'name': '', 'sourceRef': 'exclusivegateway2', 'targetRef': 'EndEvent_0ls7use'},
    'SequenceFlow_0o99twi': {'name': '', 'sourceRef': 'reportback', 'targetRef': 'EndEvent_0ls7use'}}


def get_flow(graph: diagram.BpmnDiagramGraph, user_task_id):
    flows = [(k, v) for k, v in graph.sequence_flows.items() if v['sourceRef'] == user_task_id]
    if len(flows) == 0:
        return None
    exclusive_gateway = flows[0][1]['targetRef']
    target_ref = {k: v for k, v in graph.sequence_flows.items()
                  if v['sourceRef'] == exclusive_gateway and v['name'] != ''}
    return target_ref


user_task_id = 'deptleaderaudit'
target_flows = get_flow(graph, user_task_id)
assert target_flows == {'flow3': {'name': '同意', 'sourceRef': 'exclusivegateway1', 'targetRef': 'hraudit'},
                        'flow4': {'name': '拒绝', 'sourceRef': 'exclusivegateway1', 'targetRef': 'modifyapply'}}

if __name__ == "__main__":
    pass
