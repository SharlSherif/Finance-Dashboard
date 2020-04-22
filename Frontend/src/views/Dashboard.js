/*!

=========================================================
* Black Dashboard React v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/black-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react plugin used to create charts
import { Line, Bar } from "react-chartjs-2";

// reactstrap components
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  Label,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
  UncontrolledTooltip
} from "reactstrap";

// core components
import {
  chartExample1,
  chartExample2,
  chartExample3,
  chartExample4
} from "variables/charts.js";

const API = 'http://localhost:5000/api'
class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      bigChartData: "data1",
      expensesData: {},
      earningsData: {}
    };
  }

  setBgChartData = name => {
    this.setState({
      bigChartData: name
    });
  };

  async fetchData() {
    await fetch(`${API}/dashboard?from=2020-02-01&to=2020-02-29`)
      .then(response => response.json())
      .then(data => {
        const {
          expenses_data,
          earnings_data,
          revenue,
          percentage
        } = data
        console.log(data)
        this.setState({
          expensesData: expenses_data,
          earningsData: earnings_data,
          revenue,
          percentage
        })
      })
  }

  async fetchEarningsData() {
    await fetch(`${API}/earnings?from=2020-02-01&to=2020-02-29`)
      .then(response => response.json())
      .then(earningsData => {
        console.log(earningsData)
        this.setState({
          earningsData
        })
      })
  }

  async componentDidMount() {
    await this.fetchData()
  }

  render() {
    const { expensesData, earningsData, percentage } = this.state
    return (
      <>
        <div className="content" style={{ padding: "78px 30px 30px 30px" }}>

          <Row>
            <Col lg="6">
              {!!earningsData.bar &&

                <Card className="card-chart">
                  <CardHeader>
                    <h5 className="card-category">Earnings</h5>
                    <CardTitle tag="h3" style={{ margin: 0 }}>
                      <img src={require("assets/icons/earning.svg")} width="28.45px" />{" "}
                      {earningsData.total_income}
                      <span style={{ fontSize: 15 }}> EGP</span>
                    </CardTitle>
                  </CardHeader>
                  <CardBody>
                    <div className="chart-area">
                      <Bar
                        data={{
                          labels: earningsData.bar.clients,
                          datasets: [
                            {
                              label: "Earnings",
                              fill: true,
                              borderColor: "#d048b6",
                              borderWidth: 2,
                              borderDash: [],
                              borderDashOffset: 0.0,
                              data: earningsData.bar.amounts
                            }
                          ]
                        }}
                        legend={{
                          labels: {
                            fontColor: 'rgb(255, 99, 132)'
                          }
                        }}
                        options={chartExample3.options}
                      />
                    </div>
                  </CardBody>
                </Card>
              }

            </Col>
            <Col lg="6">
              {!!expensesData.bar &&

                <Card className="card-chart">
                  <CardHeader>
                    <h5 className="card-category">Expenses</h5>
                    <CardTitle tag="h3" style={{ margin: 0 }}>
                      <img src={require("assets/icons/expense.svg")} width="28.45px" />{" "}
                      {expensesData.total_expenses}
                      <span style={{ fontSize: 15 }}> EGP</span>

                      <span style={{ fontSize: '16px', color: '#F25555', fontWeight: 500 }}> ({percentage}%)</span>
                    </CardTitle>
                  </CardHeader>
                  <CardBody>
                    <div className="chart-area">
                      <Bar
                        data={{
                          labels: expensesData.bar.categories,
                          datasets: [
                            {
                              label: "Expenses",
                              fill: true,
                              borderColor: "#d048b6",
                              borderWidth: 2,
                              borderDash: [],
                              borderDashOffset: 0.0,
                              data: expensesData.bar.amounts
                            }
                          ]
                        }}
                        legend={{
                          labels: {
                            fontColor: 'rgb(255, 99, 132)'
                          }
                        }}
                        options={chartExample3.options}
                      />
                    </div>
                  </CardBody>
                </Card>
              }

            </Col>
          </Row>
          <Row>
            <Col lg="6" md="12">
              <Card>
                <CardHeader>
                  <CardTitle tag="h4" style={{ margin: 0 }}>
                    Simple Table
                  </CardTitle>
                </CardHeader>
                <CardBody>
                  <Table className="tablesorter" responsive>
                    <thead className="text-primary">
                      <tr>
                        <th>Name</th>
                        <th>Country</th>
                        <th>City</th>
                        <th className="text-center">Salary</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Dakota Rice</td>
                        <td>Niger</td>
                        <td>Oud-Turnhout</td>
                        <td className="text-center">$36,738</td>
                      </tr>
                      <tr>
                        <td>Minerva Hooper</td>
                        <td>Curaçao</td>
                        <td>Sinaai-Waas</td>
                        <td className="text-center">$23,789</td>
                      </tr>
                      <tr>
                        <td>Sage Rodriguez</td>
                        <td>Netherlands</td>
                        <td>Baileux</td>
                        <td className="text-center">$56,142</td>
                      </tr>
                      <tr>
                        <td>Philip Chaney</td>
                        <td>Korea, South</td>
                        <td>Overland Park</td>
                        <td className="text-center">$38,735</td>
                      </tr>
                      <tr>
                        <td>Doris Greene</td>
                        <td>Malawi</td>
                        <td>Feldkirchen in Kärnten</td>
                        <td className="text-center">$63,542</td>
                      </tr>
                      <tr>
                        <td>Mason Porter</td>
                        <td>Chile</td>
                        <td>Gloucester</td>
                        <td className="text-center">$78,615</td>
                      </tr>
                      <tr>
                        <td>Jon Porter</td>
                        <td>Portugal</td>
                        <td>Gloucester</td>
                        <td className="text-center">$98,615</td>
                      </tr>
                    </tbody>
                  </Table>
                </CardBody>
              </Card>
            </Col>
            <Col lg="6" md="6">
              <Card>
                <CardHeader>
                  <CardTitle tag="h4" style={{ margin: 0 }}>Simple Table</CardTitle>
                </CardHeader>
                <CardBody>
                  <Table className="tablesorter" responsive>
                    <thead className="text-primary">
                      <tr>
                        <th>Name</th>
                        <th>Country</th>
                        <th>City</th>
                        <th className="text-center">Salary</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Dakota Rice</td>
                        <td>Niger</td>
                        <td>Oud-Turnhout</td>
                        <td className="text-center">$36,738</td>
                      </tr>
                      <tr>
                        <td>Minerva Hooper</td>
                        <td>Curaçao</td>
                        <td>Sinaai-Waas</td>
                        <td className="text-center">$23,789</td>
                      </tr>
                      <tr>
                        <td>Sage Rodriguez</td>
                        <td>Netherlands</td>
                        <td>Baileux</td>
                        <td className="text-center">$56,142</td>
                      </tr>
                      <tr>
                        <td>Philip Chaney</td>
                        <td>Korea, South</td>
                        <td>Overland Park</td>
                        <td className="text-center">$38,735</td>
                      </tr>
                      <tr>
                        <td>Doris Greene</td>
                        <td>Malawi</td>
                        <td>Feldkirchen in Kärnten</td>
                        <td className="text-center">$63,542</td>
                      </tr>
                      <tr>
                        <td>Mason Porter</td>
                        <td>Chile</td>
                        <td>Gloucester</td>
                        <td className="text-center">$78,615</td>
                      </tr>
                      <tr>
                        <td>Jon Porter</td>
                        <td>Portugal</td>
                        <td>Gloucester</td>
                        <td className="text-center">$98,615</td>
                      </tr>
                    </tbody>
                  </Table>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}

export default Dashboard;