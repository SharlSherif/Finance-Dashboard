import React from "react";
// react plugin used to create charts
import { Bar } from "react-chartjs-2";
import Select from 'react-select'
import moment from 'moment'
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Table,
  Row,
  Col,
} from "reactstrap";

// core components
import {
  chartExample3,
} from "../variables/charts.js";

const API = 'http://localhost:5000/api'
class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      bigChartData: "data1",
      expensesData: {},
      earningsData: {},
      revenue: 0,
      percentage_spent: 0,
      percentage_earned: 0,
      isLoading: true,
      date: {
        from: '2020-01-01',
        to: '2020-01-31'
      }
    };
  }

  async componentDidMount() {
    await this.fetchData(this.state.date.from, this.state.date.to)
  }

  setBgChartData = name => {
    this.setState({
      bigChartData: name
    });
  };

  async fetchData(from, to) {
    await fetch(`${API}/dashboard?from=${from}&to=${to}`)
      .then(response => { console.log(response); return response.json(); })
      .then(data => {
        const {
          expenses_data,
          earnings_data,
        } = data
        console.log(data)
        this.setState({
          expensesData: expenses_data,
          earningsData: earnings_data,
          ...data,
          isLoading: false
        })
      })
  }
  fetchNew = async () => {
    if (this.state.date.from !== '' && this.state.date.to !== '') {
      await this.fetchData(this.state.date.from, this.state.date.to)
    }
  }

  setDate = async (type, date) => {


    if (type === 'to') {
      this.setState({
        date: { to: date, from: this.state.date.from }
      }, () => {
        this.fetchNew()
      })
    } else {
      this.setState({
        date: { from: date, to: this.state.date.to }
      }, () => {
        this.fetchNew()
      })
    }


  }

  PaymentGateWay = (card) => {
    return (<div class="col-lg-2 col-md-3 col-sm-12" style={{
      marginBottom: '30px',
      maxWidth: '335px',
      marginLeft: '1%',
      boxShadow: "0px 0px 36px -23px rgba(0,0,0,0.55)",
      height: '128px', backgroundColor: 'white', borderRadius: 10,
      paddingTop: 23,
      paddingLeft: 25,
      paddingRight: 25
    }}>
      <h1 style={{
        fontSize: 20,
        fontWeight: 500,
        marginBottom: 0
      }}><img src={require("../assets/icons/credit card.svg")} width="19px" height="19px" alt="Credit Card" />  {card.name}</h1>
      <div style={{
        display: 'flex',
        marginTop: '19px'
      }}>
        <h1 style={{
          fontSize: 25,
        }}>{card.amount} EGP</h1>

      </div>

    </div>)
  }

  render() {
    const { expensesData, earningsData, percentage_earned, revenue, dates, percentage_spent, isLoading } = this.state

    if (isLoading) return ''

    const options = dates.map(date => ({ label: date, value: date }))

    const colourStyles = {
      control: styles => ({ ...styles, backgroundColor: 'white', width: '240px', margin: 'auto', marginLeft: 10, color: '#27293D' }),
    };

    return (
      <>
        <div className="content" style={{ padding: "78px 30px 30px 30px" }}>
          <div class="col-12 row">
            <h1 style={{ width: '100%', textAlign: 'center' }}> {moment(this.state.date.from).format("DD, MMM")} - {moment(this.state.date.to).format("DD, MMM")}</h1>

            <div style={{ width: '100%', textAlign: 'center', padding: 20 }}>
              <Select label="From" styles={colourStyles} options={options} onChange={e => this.setDate('from', e.value)} />
              <Select label="To" styles={colourStyles} options={options} onChange={e => this.setDate('to', e.value)} />
            </div>

            <div style={{
              marginBottom: '30px',
              maxWidth: '335px',
              boxShadow: "0px 0px 36px -23px rgba(0,0,0,0.55)",
              height: '128px', backgroundColor: 'white', borderRadius: 10,
              paddingTop: 23,
              paddingLeft: 25,
              paddingRight: 25
            }} class="col-lg-3 col-md-6 col-sm-12">
              <h1 style={{
                fontSize: 20,
                fontWeight: 500,
                marginBottom: 0
              }}><img src={require("../assets/icons/revenue.svg")} width="19px" height="19px" alt="Revenue"/>  Revenue</h1>
              <div style={{
                display: 'flex',
                marginTop: '19px'
              }} >
                <h1 class="col-7" style={{
                  fontSize: 25,
                }}>{revenue} EGP</h1>
                <span class="col-6" >

                  <div class="row">
                    {percentage_earned >= 85 ?
                      <img src={require("../assets/icons/tick mark.svg")} width="32px" height="32px" alt="Tick Mark" />
                      :
                      <img src={require("../assets/icons/x mark.svg")} width="32px" height="32px" alt="X Mark" />
                    }

                    <p style={{
                      color: percentage_earned >= 85 ? '#79DF92' : '#F25555',
                      marginLeft: '5px',
                      fontWeight: 600,
                      fontSize: '20px'
                    }}>{percentage_earned}%</p>
                  </div>

                  <p style={{ fontSize: 12, color: '#9A9A9A' }}>of total earnings</p>
                </span>
              </div>

            </div>

            {
              Object.entries(earningsData.accounts).map(([name, amount]) => {
                return this.PaymentGateWay({ name, amount })
              })
            }

          </div>
          <Row>
            <Col lg="6">
              {!!earningsData.bar &&

                <Card className="card-chart">
                  <CardHeader>
                    <h5 className="card-category">Earnings</h5>
                    <CardTitle tag="h3" style={{ margin: 0 }}>
                      <img src={require("../assets/icons/earning.svg")} width="28.45px" alt="Earnings"/>{" "}
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
                      <img src={require("../assets/icons/expense.svg")} width="28.45px" alt="Expenses"/>{" "}
                      {expensesData.total_expenses}
                      <span style={{ fontSize: 15 }}> EGP</span>

                      <span style={{ fontSize: '16px', color: '#F25555', fontWeight: 500 }}> ({percentage_spent}%)</span>
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
                  <CardTitle tag="h4" style={{ margin: 0 }}>Expenses Details</CardTitle>
                </CardHeader>
                <CardBody>
                  <Table className="tablesorter" responsive>
                    <thead className="text-primary">
                      <tr>
                        <th>Date</th>
                        <th>Client</th>
                        <th>Amount</th>
                        <th>Payment Gateway</th>
                        <th>Description</th>
                      </tr>
                    </thead>
                    <tbody>
                      {!!earningsData.table && earningsData.table.map(e => (
                        <tr>
                          <td>{e.Date}</td>
                          <td>{e['Client Name']}</td>
                          <td>{e.Amount} EGP</td>
                          <td>{e['Payment Gateway']}</td>
                          <td>{!!e['Description/Notes'] && e['Description/Notes']}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </CardBody>
              </Card>
            </Col>
            <Col lg="6" md="12">
              <Card>
                <CardHeader>
                  <CardTitle tag="h4" style={{ margin: 0 }}>Expenses Details</CardTitle>
                </CardHeader>
                <CardBody>
                  <Table className="tablesorter" responsive>
                    <thead className="text-primary">
                      <tr>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Payment Gateway</th>
                        <th>Comments</th>
                        <th >Description</th>
                      </tr>
                    </thead>
                    <tbody>
                      {!!expensesData.table && expensesData.table.map(e => (
                        <tr>
                          <td>{e.Date}</td>
                          <td>{e.Category}</td>
                          <td>{e.Amount} EGP</td>
                          <td>{e['Payment Gateway']}</td>
                          <td>{e.Comments}</td>
                          <td>{!!e['Description/Notes'] && e['Description/Notes']}</td>
                        </tr>
                      ))}
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
