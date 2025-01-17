<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('spotify_users', function (Blueprint $table) {
            $table->id();
            $table->string('spotify_id')->unique();
            $table->string('display_name')->nullable();
            $table->string('profile_image')->nullable();
            // $table->string('access_token')->nullable();
            // $table->string('refresh_token')->nullable();
            // $table->timestamp('token_expires_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('spotify_users');
    }
};
