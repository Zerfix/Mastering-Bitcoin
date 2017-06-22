

//// imports ////////////////////////////////////
// primitives
#include <string>	// text
#include <vector>	// vector
#include <iostream>	// print
#include <stdint.h>	// formated int

// threading
#include <atomic>	// primitives for multithread acsess
#include <thread>	// threading

// ssl
#include <openssl/sha.h> // crypto



//// Constants //////////////////////////////////
uint8_t CORES;
if (thread::hardware_concurrency() > 1){
	const CORES = thread::hardware_concurrency() - 1;
}
else {
	const CORES = 1;
}



//// datatypes //////////////////////////////////

// contains the results from the workers
struct result {
	std::vector<atomic_ullong, CORES> result;
	std::vector<atomic_ullong, CORES> nonce;
	std::vector<atomic_ullong, CORES> iterations = 0;
	std::atomic_short finnished = -2;
} ;

// contains previus block hash and next hash salt
typedef struct {
	std::atomic_uchar prevHash[32];
	uint64_t nonce = 0;
} __attribute__((packed)) block;



//// functions //////////////////////////////////



//// Main thread /////////////////////////////////
char proof_of_woork(uint64_t max_nonce, block working_block) {
	double difficulty;
	double difficulty_bits;
	double target;
	result res;

	std::vector<std::thread, CORES> threads;
	uint64_t iterations;

	time_t start_time;
	time_t end_time;
	
	difficulty = 2;
	for (uint64_t j = 0; j < 256; j++) {
		difficulty = difficulty * difficulty;
	}

	for (uint64_t i = 0; i < 32; i++) {
		difficulty_bits = 2;
		for (uint64_t j = 0; j < i; j++) {
			difficulty_bits = difficulty_bits * difficulty_bits;
		}

		target = difficulty - difficulty_bits;
		

		iterations = 0;

		cout << "Difficulty: " << difficulty;
		cout << "Starting shearch...";

		time(&start_time);

		// create threads
		for (uint64_t j = 0; j < CORES; j++) {
			std::thread thr(worker, working_block, j, res, difficulty, max_nonce);
			threads[j] = thr;
		}

		// wait for threads to finnish
		for (uint64_t j = 0; j < threads.size(); j++) {
			threads[j].join();
		}

		time(&end_time);

		// extract results
		for (uint64_t j = 0; j < CORES; j++) {
			iterations += res.iterations;
		}

		if (res.finnished > -1) {
			working_block.prevHash = res.result[res.finnished];
			working_block.nonce = res.nonce[res.finnished];
			cout << "Sucsess! hash found at nonce: " << to_string(working_block.nonce);
			cout << "Hash is: " << to_string(working_block.prevHash);
			cout << "Hash per seond is: " << to_string(working_block.nonce / difftime(end_time, start_time));
		}
		else if (working_block.finnished == -1) {
			cout << "found no results after " << max_nonce << "tries";
		}
		else if (working_block.finnished == -2) {
			cout << "Error: threads still running!";
		}
	}
}

// worker thread
void worker(block working_block, uint8_t thread_nr, result memory_pool, uint64_t target, uint64_t max_once) {
	char hash_result[];
	double hash_result_float;
	
	for (uint64_t i = thread_nr; i < max_once; i + CORES) {
		if (memory_pool.finnished > -2) {
			return;
		}

		working_block.nonce = i;
		memory_pool.iterations[thread_nr]++;
		
		SHA256(working_block, sizeof(block), hash_result);
		double hash_result_float = *(double*)hash_result;
		
		if (hash_result_float < target) {
			momory_pool.finnished = thread_nr;
			memory_pool.nonce[thread_nr] = nonce;
			memory_pool.result[thread_nr] = hash_result;
			release hash_result_float;
			return;
		}
	}
}



//// initialize ///////////////////////////////////////
int main() {
	cout(to_string(sizeof(block)));

	// init
	uint64_t max_once = 2 ** 63;
	
	block initial_block;
	initial_block.prevHash = "                                ";

	// compute

}
