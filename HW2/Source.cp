#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string>

#define NumL 500


#define NumI	6
#define NumH	4
#define NumO	2
#define PATH "monks.csv"


//#define NumI	16
//#define NumH	4
//#define NumO	2
//#define PATH "votes.csv"

//#define NumI	13
//#define NumH	3
//#define NumO	3
//#define PATH "wine.csv"

//#define NumI	3
//#define NumH	2
//#define NumO	2
//#define PATH "test.csv"

//#define NumI	8
//#define NumO	2
//#define PATH "hw2.5.csv"

int L = 100000;
double alpha = 0.5;
int P = 10;



double inputs[NumI + 1];
double hiddens[NumH + 1];
double outputs[NumO];
double W_hi[NumH*(NumI + 1)];
double W_oh[NumO*(NumH + 1)];




class CSVRow
{
public:
	std::string const& operator[](std::size_t index) const
	{
		return m_data[index];
	}
	std::size_t size() const
	{
		return m_data.size();
	}
	void readNextRow(std::istream& str)
	{
		std::string         line;
		std::getline(str, line);

		std::stringstream   lineStream(line);
		std::string         cell;

		m_data.clear();
		while (std::getline(lineStream, cell, ','))
		{
			m_data.push_back(cell);
		}
	}
private:
	std::vector<std::string>    m_data;
};

std::istream& operator>>(std::istream& str, CSVRow& data)
{
	data.readNextRow(str);
	return str;
}


void randomLine(int *a, int n)
{
	int index;
	int tmp;
	//srand(time(NULL));
	srand(1);
	for (int i = 0; i<n; i++)
	{
		index = rand() % (n - i) + i;
		if (index != i)
		{
			tmp = a[i];
			a[i] = a[index];
			a[index] = tmp;
		}

	}

}


void init(double* input, double* hidden, double* w_hi, double* w_oh){

	input[NumI] = 1.0;
	hidden[NumH] = 1.0;
	//srand(time(NULL));

	for (int i = 0; i < NumH; i++){

		for (int j = 0; j < NumI + 1; j++){

			w_hi[i*NumH + j]=double(rand()%100)/100.0;

		}

	}

	for (int i = 0; i < NumO; i++){
		
		for (int j = 0; j < NumH + 1; j++){

			w_oh[i*NumO + j] = double(rand() % 100) / 100.0;

		}
	}



}

void feed(double* input, double* hidden, double* output, double* w_hi, double* w_oh){

	for (int i = 0; i < NumH; i++){
	
		hidden[i] = 0;
		for (int j = 0; j < NumI+1; j++){
		
			hidden[i] += input[j] * w_hi[i*NumH + j];
		
		}
		hidden[i] = 1.0 / (1.0 + exp(-hidden[i]));
	
	}

	for (int i = 0; i < NumO; i++){
		output[i] = 0;
		for (int j = 0; j < NumH+1; j++){
		
			output[i] += hidden[j] * w_oh[i*NumO + j];
		
		}
		output[i] = 1.0 / (1.0 + exp(-output[i]));	
	}

}

void back(double* input, double* hidden, double* output, int tar, double* w_hi, double* w_oh){

	double Eo[NumO];
	double Eh[NumH];

	for (int i = 0; i < NumO; i++){
	
		if (tar == i){

			Eo[i] = (1 - output[i])*output[i] * (1 - output[i]);
		}
		else{
		
			Eo[i] = (0 - output[i])*output[i] * (1 - output[i]);
		}
	}
	for (int i = 0; i < NumH; i++){
		Eh[i] = 0.0;
		for (int j = 0; j < NumO; j++){
		
			Eh[i] += w_oh[j*NumO + i] * Eo[j];
		}
		Eh[i] = Eh[i] * hidden[i] * (1 - hidden[i]);
	
	}


	for (int i = 0; i < NumO; i++){
	
		for (int j = 0; j < NumH+1; j++){
		
			w_oh[i*NumO + j] += alpha*Eo[i] * hidden[j];
		}
	}

	for (int i = 0; i < NumH; i++){

		for (int j = 0; j < NumI + 1; j++){

			w_hi[i*NumH + j] += alpha*Eh[i] * input[j];
		}
	}




}

int maxOut(double* output){
	int maxI = 0;

	for (int i = 0; i < NumO; i++){
	
		if (output[maxI] < output[i]){
			maxI = i;
		}
	}

	return maxI;

}


double diffOut(double* output,int index){

	//double sum=0;
	//for (int i = 0; i < NumO; i++){
	//	sum += output[i] * (i + 1);
	//}
	//sum = sum / NumO;
	//return sum;
	return output[index];

}





int main()
{
	
	///////////csv parser/////////////////////////////////////////////////////
	std::ifstream in;
	in.open(PATH);
	assert(in.is_open());
	CSVRow              row;
	int count = 0;
	int rowsize;
	double matrix[NumL][NumI+1];
	double target[NumL];
	double results[NumL];
	double score[NumL];
	int matrixIndex[NumL];
	while (in >> row)
	{


		if (count == 0){
			rowsize = row.size();
		}
		else
		{ 
			for (int i = 0; i < NumI+1; i++){
			
				matrix[count-1][i] = 
atof(row[i].c_str());
				if (i != 0){
					std::cout << ",";
				}
				std::cout << matrix[count-1][i];
			}
			target[count - 1] = matrix[count - 1][NumI];
			matrix[count - 1][NumI] = 1.0;
		}
		count++;
		std::cout << "\n";
	}

	count--;
	for (int ir = 0; ir < count; ir++){
	
		matrixIndex[ir] = ir;
	}
	randomLine(matrixIndex, count);

	for (int ir = 0; ir < count; ir++){

		std::cout<<matrixIndex[ir]<<",";
	}
	std::cout << "\n";
	////////////////////////////////////////////////////

	int halfCount = round(double(count) / 2.0);
	int tenthCount = floor(double(count) / 10.0);
	init(inputs,hiddens,W_hi,W_oh);
	for (int k = 0; k < L; k++)
	{

		for (int rc = 0; rc < count; rc++){

			//for (int k = 0; k < NumI; k++){
			//
			//	inputs[k] = matrix[c][k];
			//	/*std::cout << inputs[k] << ",";*/
			//}
			//std::cout << inputs[NumI];
			/*std::cout << "\n";*/
			if (rc<tenthCount*(P - 1) || rc>tenthCount*P)
			{	
				int c = matrixIndex[rc];
				feed(&matrix[c][0], hiddens, outputs, W_hi, W_oh);
				back(&matrix[c][0], hiddens, outputs, target[c], W_hi, W_oh);
			}

			//feed(inputs, hiddens, outputs, W_hi, W_oh);
			//back(inputs, hiddens, outputs, target[c], W_hi, W_oh);

			//for (int k = 0; k < NumI+1; k++){
			//	std::cout << W_hi[k] << ",";
			//
			//}
			//std::cout << "\n";
			//results[c]= maxOut(outputs);
		}
	
	}



	for (int rc = 0; rc < count; rc++){

		int c = matrixIndex[rc];
		feed(&matrix[c][0], hiddens, outputs, W_hi, W_oh);
		results[c] = maxOut(outputs);
		score[c] = diffOut(outputs,0);
	}


	double e = 0.0;
	std::cout << "\n training error\n";
	for (int rc = 0; rc < count; rc++){
		if (rc<tenthCount*(P - 1) ||rc>tenthCount*P)
		{
			int c = matrixIndex[rc];
			std::cout << score[c] << "," << target[c] << ";";
			if (results[c] != target[c])
			e++;
		}

	}
	std::cout << "\n";
	std::cout << e / count << "\n";

	e = 0.0;
	std::cout << "\n test error\n";
	for (int rc = 0; rc < count; rc++){
		if (rc>=tenthCount*(P - 1) && rc<=tenthCount*P)
		{
			int c = matrixIndex[rc];
			std::cout << score[c] << "," << target[c] << ";";
			if (results[c] != target[c])
				e++;
		}
	}
	std::cout << "\n";
	std::cout << e / count << "\n";


	/*feed(inputs, hidden, outputs, w_hi, w_oh);*/
	//std::cout << "\n";
	//for (int i = 0; i < NumO; i++){
	//	std::cout << outputs[i] << ",";
	//
	//}
	//std::cout << "\n";





	getchar();



}
